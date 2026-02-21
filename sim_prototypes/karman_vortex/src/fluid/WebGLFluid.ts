import * as Shaders from './shaders';

type WebGLProgramInfo = {
    program: WebGLProgram;
    uniforms: Record<string, WebGLUniformLocation | null>;
};

class FBO {
    texture: WebGLTexture;
    fbo: WebGLFramebuffer;
    width: number;
    height: number;
    texelSizeX: number;
    texelSizeY: number;

    constructor(gl: WebGLRenderingContext, width: number, height: number, internalFormat: number, format: number, type: number) {
        this.width = width;
        this.height = height;
        this.texelSizeX = 1.0 / width;
        this.texelSizeY = 1.0 / height;

        gl.activeTexture(gl.TEXTURE0);
        const texture = gl.createTexture();
        if (!texture) throw new Error("Texture creation failed");
        gl.bindTexture(gl.TEXTURE_2D, texture);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texImage2D(gl.TEXTURE_2D, 0, internalFormat, width, height, 0, format, type, null);
        this.texture = texture;

        const fbo = gl.createFramebuffer();
        if (!fbo) throw new Error("FBO creation failed");
        gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0);
        gl.viewport(0, 0, width, height);
        gl.clear(gl.COLOR_BUFFER_BIT);
        this.fbo = fbo;
    }
}

class DoubleFBO {
    read: FBO;
    write: FBO;
    constructor(gl: WebGLRenderingContext, width: number, height: number, internalFormat: number, format: number, type: number) {
        this.read = new FBO(gl, width, height, internalFormat, format, type);
        this.write = new FBO(gl, width, height, internalFormat, format, type);
    }
    swap() {
        const temp = this.read;
        this.read = this.write;
        this.write = temp;
    }
}

export class WebGLFluid {
    canvas: HTMLCanvasElement;
    gl: WebGLRenderingContext;
    ext: any;

    width: number;
    height: number;
    aspectRatio: number;

    density!: DoubleFBO;
    velocity!: DoubleFBO;
    divergenceC!: FBO;
    pressure!: DoubleFBO;

    advectionProgram!: WebGLProgramInfo;
    divergenceProgram!: WebGLProgramInfo;
    pressureProgram!: WebGLProgramInfo;
    gradientSubtractProgram!: WebGLProgramInfo;
    splatProgram!: WebGLProgramInfo;
    displayProgram!: WebGLProgramInfo;
    constantInflowProgram!: WebGLProgramInfo;

    obstacleCenter = { x: 0.5, y: 0.5 };
    obstacleRadius = 0.05;
    windSpeed = 2.0;
    viscosity = 0.5;

    private lastTime: number = 0;
    private reqId: number = 0;

    constructor(canvas: HTMLCanvasElement) {
        this.canvas = canvas;
        const gl = canvas.getContext('webgl', { alpha: false, depth: false, stencil: false, antialias: false });
        if (!gl) throw new Error("WebGL not supported");
        this.gl = gl;

        this.ext = gl.getExtension('OES_texture_half_float') || gl.getExtension('OES_texture_float');
        gl.getExtension('OES_texture_half_float_linear') || gl.getExtension('OES_texture_float_linear');

        this.width = canvas.width;
        this.height = canvas.height;
        this.aspectRatio = this.width / this.height;

        gl.clearColor(0.0, 0.0, 0.0, 1.0);

        this.initFBOs();
        this.initShaders();
    }

    resize(width: number, height: number) {
        this.canvas.width = width;
        this.canvas.height = height;
        this.width = width;
        this.height = height;
        this.aspectRatio = width / height;
        this.initFBOs();
    }

    private initFBOs() {
        const { gl, ext, width, height } = this;
        const simResX = Math.floor(width / 4);
        const simResY = Math.floor(height / 4);

        const type = ext && ext.HALF_FLOAT_OES ? ext.HALF_FLOAT_OES : gl.FLOAT;

        this.density = new DoubleFBO(gl, simResX, simResY, gl.RGBA, gl.RGBA, type);
        this.velocity = new DoubleFBO(gl, simResX, simResY, gl.RGBA, gl.RGBA, type);
        this.divergenceC = new FBO(gl, simResX, simResY, gl.RGBA, gl.RGBA, type);
        this.pressure = new DoubleFBO(gl, simResX, simResY, gl.RGBA, gl.RGBA, type);
    }

    private createProgram(vertexShaderSource: string, fragmentShaderSource: string): WebGLProgramInfo {
        const gl = this.gl;
        const vs = gl.createShader(gl.VERTEX_SHADER)!;
        gl.shaderSource(vs, vertexShaderSource);
        gl.compileShader(vs);

        const fs = gl.createShader(gl.FRAGMENT_SHADER)!;
        gl.shaderSource(fs, fragmentShaderSource);
        gl.compileShader(fs);

        const program = gl.createProgram()!;
        gl.attachShader(program, vs);
        gl.attachShader(program, fs);
        gl.linkProgram(program);

        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            console.error(gl.getProgramInfoLog(program));
        }

        const uniforms: Record<string, WebGLUniformLocation | null> = {};
        const uniformCount = gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS);
        for (let i = 0; i < uniformCount; i++) {
            const uniformName = gl.getActiveUniform(program, i)!.name;
            uniforms[uniformName] = gl.getUniformLocation(program, uniformName);
        }

        return { program, uniforms };
    }

    private initShaders() {
        this.advectionProgram = this.createProgram(Shaders.baseVertexShader, Shaders.advectionShaderSource);
        this.divergenceProgram = this.createProgram(Shaders.baseVertexShader, Shaders.divergenceShaderSource);
        this.pressureProgram = this.createProgram(Shaders.baseVertexShader, Shaders.pressureShaderSource);
        this.gradientSubtractProgram = this.createProgram(Shaders.baseVertexShader, Shaders.gradientSubtractShaderSource);
        this.splatProgram = this.createProgram(Shaders.baseVertexShader, Shaders.splatShaderSource);
        this.displayProgram = this.createProgram(Shaders.baseVertexShader, Shaders.displayShaderSource);
        this.constantInflowProgram = this.createProgram(Shaders.baseVertexShader, Shaders.constantInflowShaderSource);

        const gl = this.gl;
        const vertexBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, -1, 1, 1, 1, 1, -1]), gl.STATIC_DRAW);

        // We bind the attribute locations once, assuming all programs use 'aPosition' at index 0
        const aPosition = 0;
        gl.enableVertexAttribArray(aPosition);
        gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, 0, 0);
    }

    private bindProgram(programInfo: WebGLProgramInfo) {
        this.gl.useProgram(programInfo.program);
        this.gl.uniform2f(programInfo.uniforms.texelSize, this.velocity.read.texelSizeX, this.velocity.read.texelSizeY);
        if (programInfo.uniforms.obstacleCenter) {
            this.gl.uniform2f(programInfo.uniforms.obstacleCenter, this.obstacleCenter.x, this.obstacleCenter.y);
            this.gl.uniform1f(programInfo.uniforms.obstacleRadius, this.obstacleRadius);
            this.gl.uniform1f(programInfo.uniforms.aspectRatio, this.aspectRatio);
        }
    }

    private blit(target: FBO | null) {
        const gl = this.gl;
        if (target == null) {
            gl.viewport(0, 0, this.width, this.height);
            gl.bindFramebuffer(gl.FRAMEBUFFER, null);
        } else {
            gl.viewport(0, 0, target.width, target.height);
            gl.bindFramebuffer(gl.FRAMEBUFFER, target.fbo);
        }
        // We draw the quad 
        const indexBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array([0, 1, 2, 0, 2, 3]), gl.STATIC_DRAW);
        gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, 0);
        gl.deleteBuffer(indexBuffer);
    }

    splat(x: number, y: number, dx: number, dy: number, color: { r: number, g: number, b: number }) {
        const gl = this.gl;
        this.bindProgram(this.splatProgram);
        gl.uniform2f(this.splatProgram.uniforms.point, x, 1.0 - y);
        gl.uniform1f(this.splatProgram.uniforms.aspectRatio, this.aspectRatio);
        gl.uniform1f(this.splatProgram.uniforms.radius, 0.005);

        // Splat velocity
        gl.uniform3f(this.splatProgram.uniforms.color, dx * 5.0, -dy * 5.0, 0.0);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.velocity.read.texture);
        gl.uniform1i(this.splatProgram.uniforms.uTarget, 0);
        this.blit(this.velocity.write);
        this.velocity.swap();

        // Splat density
        gl.uniform3f(this.splatProgram.uniforms.color, color.r, color.g, color.b);
        gl.bindTexture(gl.TEXTURE_2D, this.density.read.texture);
        gl.uniform1i(this.splatProgram.uniforms.uTarget, 0);
        this.blit(this.density.write);
        this.density.swap();
    }

    private applyConstantInflow() {
        const gl = this.gl;
        this.bindProgram(this.constantInflowProgram);

        // Inflow Velocity
        gl.uniform1f(this.constantInflowProgram.uniforms.isVelocity, 1.0);
        gl.uniform2f(this.constantInflowProgram.uniforms.inflowVelocity, this.windSpeed, 0.0);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.velocity.read.texture);
        gl.uniform1i(this.constantInflowProgram.uniforms.uTarget, 0);
        this.blit(this.velocity.write);
        this.velocity.swap();

        // Inflow Dye
        gl.uniform1f(this.constantInflowProgram.uniforms.isVelocity, 0.0);
        // Cyan / Magenta neon color alternating slightly or constant over time
        const r = Math.sin(Date.now() * 0.001) * 0.5 + 0.5;
        gl.uniform3f(this.constantInflowProgram.uniforms.inflowColor, 0.2, 0.8 + r * 0.2, 1.0);
        gl.bindTexture(gl.TEXTURE_2D, this.density.read.texture);
        gl.uniform1i(this.constantInflowProgram.uniforms.uTarget, 0);
        this.blit(this.density.write);
        this.density.swap();
    }

    private step(dt: number) {
        const gl = this.gl;
        gl.disable(gl.BLEND);

        this.applyConstantInflow();

        // Advection
        this.bindProgram(this.advectionProgram);
        gl.uniform1f(this.advectionProgram.uniforms.dt, dt);
        gl.uniform1f(this.advectionProgram.uniforms.dissipation, 0.0); // Velocity dissipation
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.velocity.read.texture);
        gl.uniform1i(this.advectionProgram.uniforms.uVelocity, 0);
        gl.activeTexture(gl.TEXTURE1);
        gl.bindTexture(gl.TEXTURE_2D, this.velocity.read.texture);
        gl.uniform1i(this.advectionProgram.uniforms.uSource, 1);
        this.blit(this.velocity.write);
        this.velocity.swap();

        gl.uniform1f(this.advectionProgram.uniforms.dissipation, this.viscosity); // Density (viscosity slider actually controls dye dissipation for visuals here)
        gl.activeTexture(gl.TEXTURE1);
        gl.bindTexture(gl.TEXTURE_2D, this.density.read.texture);
        gl.uniform1i(this.advectionProgram.uniforms.uSource, 1);
        this.blit(this.density.write);
        this.density.swap();

        // Divergence
        this.bindProgram(this.divergenceProgram);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.velocity.read.texture);
        gl.uniform1i(this.divergenceProgram.uniforms.uVelocity, 0);
        this.blit(this.divergenceC);

        // Clear pressure
        gl.bindFramebuffer(gl.FRAMEBUFFER, this.pressure.read.fbo);
        gl.clear(gl.COLOR_BUFFER_BIT);

        // Pressure Solver (Jacobi iteration)
        this.bindProgram(this.pressureProgram);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.divergenceC.texture);
        gl.uniform1i(this.pressureProgram.uniforms.uDivergence, 0);
        for (let i = 0; i < 20; i++) {
            gl.activeTexture(gl.TEXTURE1);
            gl.bindTexture(gl.TEXTURE_2D, this.pressure.read.texture);
            gl.uniform1i(this.pressureProgram.uniforms.uPressure, 1);
            this.blit(this.pressure.write);
            this.pressure.swap();
        }

        // Gradient Subtract
        this.bindProgram(this.gradientSubtractProgram);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.pressure.read.texture);
        gl.uniform1i(this.gradientSubtractProgram.uniforms.uPressure, 0);
        gl.activeTexture(gl.TEXTURE1);
        gl.bindTexture(gl.TEXTURE_2D, this.velocity.read.texture);
        gl.uniform1i(this.gradientSubtractProgram.uniforms.uVelocity, 1);
        this.blit(this.velocity.write);
        this.velocity.swap();
    }

    private render() {
        const gl = this.gl;
        this.bindProgram(this.displayProgram);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.density.read.texture);
        gl.uniform1i(this.displayProgram.uniforms.uTexture, 0);
        this.blit(null);
    }

    public update(time: number) {
        if (this.lastTime === 0) this.lastTime = time;
        let dt = (time - this.lastTime) * 0.001;
        dt = Math.min(dt, 0.016); // cap at 60fps equivalent
        this.lastTime = time;

        this.step(dt);
        this.render();

        this.reqId = requestAnimationFrame((t) => this.update(t));
    }

    public start() {
        if (this.reqId === 0) {
            this.reqId = requestAnimationFrame((t) => this.update(t));
        }
    }

    public stop() {
        cancelAnimationFrame(this.reqId);
        this.reqId = 0;
    }
}
