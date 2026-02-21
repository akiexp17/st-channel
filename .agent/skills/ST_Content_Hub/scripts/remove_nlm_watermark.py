#!/usr/bin/env python3
"""
NotebookLM動画からウォーターマークを除去するスクリプト。

処理内容:
  1. 右下の「NotebookLM」テキスト+アイコン → drawboxフィルターで白塗り
  2. 末尾の「notebooklm.google.com」画面 → カットして削除
  3. Short動画（_short を含むファイル）→ 9:16縦長に中央クロップ（--portrait 指定時）

Usage:
    python3 remove_nlm_watermark.py --input video.mp4 [--output video_clean.mp4]
    python3 remove_nlm_watermark.py --dir 04_Media/videos/ --in-place
    python3 remove_nlm_watermark.py --dir 04_Media/videos/ --in-place --portrait  # Short動画を9:16に
"""

import argparse
import glob
import json
import os
import subprocess
import sys


def get_video_info(path: str) -> dict:
    """ffprobeで動画のメタ情報を取得"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", "-show_format",
        path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    video_stream = next(s for s in data["streams"] if s["codec_type"] == "video")
    return {
        "width": int(video_stream["width"]),
        "height": int(video_stream["height"]),
        "duration": float(data["format"]["duration"]),
        "fps": video_stream.get("r_frame_rate", "24/1"),
    }


def detect_end_card_start(path: str, duration: float) -> float:
    """
    末尾のnotebooklm.google.comエンドカードが開始するタイムスタンプを検出。
    最後の10秒の各フレームの平均輝度差を分析し、
    ほぼ白い静止画面（エンドカード）への遷移を検出する。
    """
    # 末尾10秒からシーンチェンジを検出
    start_check = max(0, duration - 12)
    cmd = [
        "ffprobe", "-v", "quiet",
        "-f", "lavfi",
        "-i", f"movie={path},select='gt(scene\\,0.3)',showinfo",
        "-show_entries", "frame=pts_time",
        "-of", "csv=p=0",
        "-read_intervals", f"{start_check}%+12"
    ]
    # フォールバック: 末尾5秒をカット
    fallback = duration - 5.0

    try:
        # シーンチェンジ検出の代わりに、末尾フレームの平均色をチェック
        # NotebookLMのエンドカードはほぼ白い背景
        check_times = [duration - t for t in range(1, 11)]
        for t in sorted(check_times):
            cmd_check = [
                "ffmpeg", "-ss", str(t), "-i", path,
                "-frames:v", "1", "-vf",
                "crop=200:50:540:380,format=gray,blackframe=amount=0:threshold=240",
                "-f", "null", "-"
            ]
            result = subprocess.run(cmd_check, capture_output=True, text=True, timeout=10)
            # blackframeが検出された = ほぼ白い画面
            if "Parsed_blackframe" in result.stderr and "[Parsed_blackframe" in result.stderr:
                # このフレームはほぼ白 → エンドカードの一部
                continue
            else:
                # コンテンツの始まり。この直後がエンドカード開始
                return t + 0.5
    except Exception:
        pass

    return fallback


def remove_watermark(input_path: str, output_path: str, trim_end_card: bool = True, portrait: bool = False) -> bool:
    """
    動画からNotebookLMのウォーターマークを除去。

    1. drawboxフィルターで右下のロゴを白塗り
    2. 末尾のエンドカード（notebooklm.google.com）をカット
    3. portrait=Trueの場合、16:9→9:16に中央クロップ
    """
    info = get_video_info(input_path)
    w, h = info["width"], info["height"]
    duration = info["duration"]

    is_short = "_short" in os.path.basename(input_path)
    do_portrait = portrait and is_short

    mode_str = " [9:16変換]" if do_portrait else ""
    print(f"  📐 {w}x{h}, {duration:.1f}s{mode_str}")

    # フィルターチェーン構築
    filters = []

    # 1. ウォーターマーク除去（drawbox白塗り）
    logo_x = int(w * 1040 / 1280)
    logo_y = int(h * 660 / 720)
    logo_w = int(w * 240 / 1280)
    logo_h = int(h * 60 / 720)
    filters.append(f"drawbox=x={logo_x}:y={logo_y}:w={logo_w}:h={logo_h}:color=white@1:t=fill")

    # 2. 9:16縦長クロップ（Short動画のみ）
    if do_portrait:
        # 16:9 → 9:16 : 中央から縦長部分をクロップ
        # 入力: 1280x720 → 出力: 405x720 (9:16比率) → スケール: 720x1280
        crop_w = int(h * 9 / 16)  # 720 * 9/16 = 405
        crop_x = (w - crop_w) // 2  # 中央
        filters.append(f"crop={crop_w}:{h}:{crop_x}:0")
        filters.append(f"scale=720:1280:flags=lanczos")

    vf = ",".join(filters)

    # 末尾エンドカードのカット
    trim_duration = None
    if trim_end_card:
        trim_duration = duration - 3.0
        if trim_duration < duration * 0.9:
            print(f"  ⚠️ エンドカード検出をスキップ（カット量が大きすぎる）")
            trim_duration = None

    # ffmpegコマンド構築
    cmd = ["ffmpeg", "-y", "-i", input_path]

    if trim_duration:
        cmd.extend(["-t", f"{trim_duration:.2f}"])

    cmd.extend([
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path
    ])

    print(f"  🔧 処理中...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if result.returncode == 0:
        orig_size = os.path.getsize(input_path) / (1024 * 1024)
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        out_info = get_video_info(output_path)
        print(f"  ✅ 完了: {orig_size:.1f}MB → {new_size:.1f}MB ({out_info['width']}x{out_info['height']})")
        return True
    else:
        print(f"  ❌ エラー: {result.stderr[-200:]}")
        return False


def process_directory(dir_path: str, suffix: str = "_clean", in_place: bool = False, portrait: bool = False):
    """ディレクトリ内の全mp4を処理"""
    files = sorted(glob.glob(os.path.join(dir_path, "*.mp4")))

    if not files:
        print(f"❌ {dir_path} にmp4ファイルが見つかりません")
        return

    # _clean が既についているファイルはスキップ
    files = [f for f in files if "_clean" not in f]

    portrait_str = " + Short動画9:16変換" if portrait else ""
    print(f"\n🎬 NotebookLM ウォーターマーク除去{portrait_str}")
    print(f"=" * 60)
    print(f"  対象: {len(files)} ファイル")
    print()

    results = {"success": [], "failed": []}

    for f in files:
        basename = os.path.basename(f)
        print(f"📁 {basename}")

        if in_place:
            tmp_output = f + ".tmp.mp4"
            success = remove_watermark(f, tmp_output, portrait=portrait)
            if success:
                os.replace(tmp_output, f)
                results["success"].append(basename)
            else:
                if os.path.exists(tmp_output):
                    os.remove(tmp_output)
                results["failed"].append(basename)
        else:
            name, ext = os.path.splitext(f)
            output = f"{name}{suffix}{ext}"
            success = remove_watermark(f, output, portrait=portrait)
            if success:
                results["success"].append(basename)
            else:
                results["failed"].append(basename)

    print(f"\n{'=' * 60}")
    print(f"✅ 成功: {len(results['success'])} / {len(files)}")
    if results["failed"]:
        print(f"❌ 失敗: {', '.join(results['failed'])}")


def main():
    parser = argparse.ArgumentParser(description="NotebookLMウォーターマーク除去")
    parser.add_argument("--input", "-i", help="入力ファイル")
    parser.add_argument("--output", "-o", help="出力ファイル")
    parser.add_argument("--dir", "-d", help="ディレクトリ内の全mp4を処理")
    parser.add_argument("--in-place", action="store_true", help="元ファイルを上書き")
    parser.add_argument("--no-trim", action="store_true", help="末尾エンドカードのカットをスキップ")
    parser.add_argument("--portrait", action="store_true", help="Short動画(_short含む)を9:16縦長に変換")
    args = parser.parse_args()

    if args.dir:
        process_directory(args.dir, in_place=args.in_place, portrait=args.portrait)
    elif args.input:
        output = args.output or args.input.replace(".mp4", "_clean.mp4")
        remove_watermark(args.input, output, trim_end_card=not args.no_trim, portrait=args.portrait)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
