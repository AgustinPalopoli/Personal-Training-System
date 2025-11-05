function ventanamodal() {
    const modal_container = document.getElementById('modal_container_final');
    const close = document.getElementById('close');
    modal_container.style.opacity = "1";
    modal_container.style.pointerEvents = "auto";
    close.addEventListener('click', () => {
      modal_container.style.opacity = "0";
      modal_container.style.pointerEvents = "none";
    });
}

function descanso_sonido(){
    let myAudio = document.querySelector('#audio')
    myAudio.play()
};
function mostrar_imagen(id,url) {
    var cambiar = document.getElementById(`derecha_rutina${parseInt(id,10)}`)
    var dir = "static/plataforma/imagenes/" + url 
    dir = `<img class="img_rutina" src="${dir}" >`
    cambiar.innerHTML = dir
};

function cambiarpeso(id,ej,cantidad){
    var cambiar = document.getElementById(`peso${parseInt(id,10)}`)
    cambiar.onclick = ""
    cambiar.innerHTML = `<b>Peso: </b><input style="margin-bottom:1vh;" id="i${id}" class="botonP btn btn-secondary" autocomplete="off" autofocus name="cantidad_peso" value="${cantidad}" type="text"><button ondblclick="volver('${id}','${ej}','${cantidad}')" class="botonP btn btn-primary" type="submit"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-floppy-fill" viewBox="0 0 16 16"><path d="M0 1.5A1.5 1.5 0 0 1 1.5 0H3v5.5A1.5 1.5 0 0 0 4.5 7h7A1.5 1.5 0 0 0 13 5.5V0h.086a1.5 1.5 0 0 1 1.06.44l1.415 1.414A1.5 1.5 0 0 1 16 2.914V14.5a1.5 1.5 0 0 1-1.5 1.5H14v-5.5A1.5 1.5 0 0 0 12.5 9h-9A1.5 1.5 0 0 0 2 10.5V16h-.5A1.5 1.5 0 0 1 0 14.5v-13Z"/><path d="M3 16h10v-5.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5V16Zm9-16H4v5.5a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 .5-.5V0ZM9 1h2v4H9V1Z"/></svg></button><input style="display:none" name="ejercicio_id" value="${ej}">`
};

function volver(id,ej,cantidad){
    var cambiar = document.getElementById(`peso${parseInt(id,10)}`)
    cambiar.innerHTML = "<b>Peso: </b>" + document.getElementById(`i${parseInt(id,10)}`).value
};

function descansaa(id,tiempo){
    var seriesA = document.getElementById(`seriesA${parseInt(id,10)}`)
    var seriesT = document.getElementById(`seriesT${parseInt(id,10)}`)
    seriesA.textContent = parseInt(seriesA.textContent,10) + 1
    var timer = document.getElementById(parseInt(id,10));
    timer.innerHTML = `<span style="font-size:40px" id="${"M"+id}">0${tiempo[3]}</span><span style="font-size:40px" >:</span><span style="font-size:40px" id="${"S"+id}">${tiempo.slice(5, 7)}</span>`;
    var timeleft = parseInt(tiempo.slice(5, 7),10);
    var flag = 0;
    minutos = document.getElementById("M"+id);
    segundos = document.getElementById("S"+id);
    var downloadTimer = setInterval(function(){
        if(timeleft <= 0){
            if (tiempo[3] != 0){
                if (flag == 0){
                    timeleft = tiempo[3] * 60;
                    minutos.textContent = "00" 
                    flag = 1;
                }
                else{
                    if ((parseInt(seriesA.textContent,10) + 1) == parseInt(seriesT.textContent,10)){
                        descanso_sonido()
                        timer.innerHTML = `<button class="btn btn-success" type="button" id="descanso" onclick="listo('${id}')" ><b>Listo</b><svg style="margin-left:1vh" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16"><path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z"/></svg></button>`
                    }
                    else{
                        descanso_sonido()
                        timer.innerHTML = `<button class="btn btn-warning" type="button" id="descanso" onclick="descansaa('${id}','${tiempo}')" ><b>Descanso</b><svg style="margin-left:1vh" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg></button>`
                    }
                    clearInterval(downloadTimer);
                }
            }
            else{
                if ((parseInt(seriesA.textContent,10) + 1) == parseInt(seriesT.textContent,10)){
                    descanso_sonido()
                    timer.innerHTML = `<button class="btn btn-success" type="button" id="descanso" onclick="listo('${id}')" ><b>Listo</b><svg style="margin-left:1vh" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16"><path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z"/></svg></button>`
                }
                else{
                    descanso_sonido()
                    timer.innerHTML = `<button class="btn btn-warning"  type="button" id="descanso" onclick="descansaa('${id}','${tiempo}')" ><b>Descanso</b><svg style="margin-left:1vh" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg></button>`
                }
                clearInterval(downloadTimer);
            };
        };
        if (timeleft < 10){
            segundos.textContent = "0" + timeleft;
        }
        else{
            segundos.textContent = timeleft;
        }
        timeleft--;
    },1000)
};

function confetti(){
    let W = window.innerWidth;
    let H = document.getElementById('confetti').clientHeight;
    const canvas = document.getElementById('confetti');
    const context = canvas.getContext("2d");
    const maxConfettis = 25;
    const particles = [];

    const possibleColors = [
        "#ff7336",
        "#f9e038",
        "#02cca4",
        "#383082",
        "#fed3f5",
        "#b1245a",
        "#f2733f"
    ];

    function randomFromTo(from, to) {
        return Math.floor(Math.random() * (to - from + 1) + from);
    }

    function confettiParticle() {
        this.x = Math.random() * W; // x
        this.y = Math.random() * H - H; // y
        this.r = randomFromTo(11, 33); // radius
        this.d = Math.random() * maxConfettis + 11;
        this.color =
            possibleColors[Math.floor(Math.random() * possibleColors.length)];
        this.tilt = Math.floor(Math.random() * 33) - 11;
        this.tiltAngleIncremental = Math.random() * 0.07 + 0.05;
        this.tiltAngle = 0;

        this.draw = function() {
            context.beginPath();
            context.lineWidth = this.r / 2;
            context.strokeStyle = this.color;
            context.moveTo(this.x + this.tilt + this.r / 3, this.y);
            context.lineTo(this.x + this.tilt, this.y + this.tilt + this.r / 5);
            return context.stroke();
        };
    }

    function Draw() {
    const results = [];

    // Magical recursive functional love
    requestAnimationFrame(Draw);

    context.clearRect(0, 0, W, window.innerHeight);

    for (var i = 0; i < maxConfettis; i++) {
        results.push(particles[i].draw());
    }

    let particle = {};
    let remainingFlakes = 0;
    for (var i = 0; i < maxConfettis; i++) {
        particle = particles[i];

        particle.tiltAngle += particle.tiltAngleIncremental;
        particle.y += (Math.cos(particle.d) + 3 + particle.r / 2) / 2;
        particle.tilt = Math.sin(particle.tiltAngle - i / 3) * 15;

        if (particle.y <= H) remainingFlakes++;

        // If a confetti has fluttered out of view,
        // bring it back to above the viewport and let if re-fall.
        if (particle.x > W + 30 || particle.x < -30 || particle.y > H) {
        particle.x = Math.random() * W;
        particle.y = -30;
        particle.tilt = Math.floor(Math.random() * 10) - 20;
        }
    }

    return results;
    }

    window.addEventListener(
    "resize",
    function() {
        W = window.innerWidth;
        H = window.innerHeight;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    },
    false
    );

    // Push new confetti objects to `particles[]`
    for (var i = 0; i < maxConfettis; i++) {
        particles.push(new confettiParticle());
    }

    // Initialize
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.position = "absolute";
    canvas.style.display = "block";
    Draw();
}


function listo(id){
    var seriesA = document.getElementById(`seriesA${parseInt(id,10)}`)
    document.getElementById(`collap${parseInt(id,10)}`).style.backgroundColor = "green";
    seriesA.textContent = parseInt(seriesA.textContent,10) + 1;
    var timer = document.getElementById(parseInt(id,10));
    timer.innerHTML = "";
    var coll = document.getElementsByClassName("collapsible");
    if(coll[coll.length - 1].id == (`collap${parseInt(id,10)}`)){
        let myAudio = document.querySelector('#audio_final')
        myAudio.play()
        ventanamodal()
        confetti()
    }
};