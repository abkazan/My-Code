"use strict";
const stars_x = []
const stars_y = []



//console.log(slider.value)
// direction variable: 
//    if the ship is going right, dir is >1
//    if the ship is going left, dir is <1
var canvas = document.getElementById('myCanvas');
// for moving the ship
var x = 0;
// for moving the lasers
var y = 0;
// for moving stars
var star_x = 0;
var star_y = 0;
var dir = 3;
var star_dir = .25;
var stars_gen = 0;

function draw() {
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, 400, 400);
    function DrawStars(x_start, y_start, color) {
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(x_start, y_start);
        ctx.lineTo(x_start, y_start + 1);
        ctx.lineTo(x_start + 1, y_start + 1);
        ctx.lineTo(x_start + 1, y_start);
        ctx.closePath()
        ctx.fill();
    }
    function DrawBackgroud(color) {
        ctx.save();
        /*
        for (let i = 0; i < 100; i++) {
            var rand_x = Math.floor(Math.random() * star_x) - 20;
            var rand_y = Math.floor(Math.random() * star_y) - 20;
            DrawStars(rand_x, rand_y, "white")
        }
        */
        ctx.translate(star_x, star_y);
        // find area of blank space and

        // we want at least 100 stars
        // draw 100 random stars
        if (stars_gen === 0) {
            for (let i = 0; i < 200; i++) {
                var rand_x = Math.floor(Math.random() * 420) - 20;
                var rand_y = Math.floor(Math.random() * 420) - 20;
                stars_x.push(rand_x);
                stars_y.push(rand_y);
            }
            for (let i = 0; i < 200; i++) {
                DrawStars(stars_x[i], stars_y[i], "white")
                /*
                //generate a random number between 0 and 100
                var rand_color = Math.floor(Math.random() * 100);
                if (rand_color % 10 === 0) {
                    DrawStars(stars_x[i], stars_y[i], "gray")
                } else {
                    DrawStars(stars_x[i], stars_y[i], "white")
                } 
                */
            }
            stars_gen++
        } else {
            for (let i = 0; i < 200; i++) {
                var rand_color = Math.floor(Math.random() * 100);
                DrawStars(stars_x[i], stars_y[i], "white")
                /*
                if (rand_color % 10 === 0) {
                    DrawStars(stars_x[i], stars_y[i], "gray")
                } else {
                    DrawStars(stars_x[i], stars_y[i], "white")
                }
                */
            }
        }
        /*
        for (let i = -20; i < 420; i += 20) {
            for (let j = -20; j < 420; j+=20) {
                
                console.log(rand)
                DrawStars(i,j,"white")
            }
        }
        */
        ctx.restore();
    }
    function DrawWings(color) {
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(50, 250);
        ctx.lineTo(60, 250);
        ctx.lineTo(58, 190);
        ctx.lineTo(52, 190);
        ctx.moveTo(150, 250);
        ctx.lineTo(160, 250);
        ctx.lineTo(158, 190);
        ctx.lineTo(152, 190);
        ctx.closePath();
        ctx.fill();
    }
    function DrawBase(color) {
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(50, 245);
        ctx.lineTo(160, 245);
        ctx.lineTo(160, 285);
        ctx.lineTo(50, 285);
        ctx.closePath();
        ctx.fill();
    }
    function DrawEngines(color) {
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(50, 285);
        ctx.lineTo(50, 295);
        ctx.lineTo(75, 295);
        ctx.lineTo(75, 285);
        ctx.moveTo(160, 285);
        ctx.lineTo(160, 295);
        ctx.lineTo(135, 295);
        ctx.lineTo(135, 285);
        ctx.closePath();
        ctx.fill();

    }
    function DrawHead(color) {
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(95, 250);
        ctx.lineTo(115, 250);
        ctx.lineTo(110, 130);
        ctx.lineTo(100, 130);
        ctx.closePath();
        ctx.fill();
    }
    function DrawX(color) {
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(30, 240);
        ctx.lineTo(180, 280);
        ctx.lineTo(175, 290);
        ctx.lineTo(25, 250);
        ctx.moveTo(180, 240);
        ctx.lineTo(30, 280);
        ctx.lineTo(35, 290);
        ctx.lineTo(185, 250);
        ctx.closePath();
        ctx.fill();
    }
    function DrawLasers(color) {
        ctx.save();
        ctx.translate(0, -y);
        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.moveTo(152, 190);
        ctx.lineTo(152, 170);
        ctx.lineTo(157, 170);
        ctx.lineTo(157, 190);
        ctx.moveTo(52, 190);
        ctx.lineTo(52, 170);
        ctx.lineTo(57, 170);
        ctx.lineTo(57, 190);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
    
    ctx.save();
    DrawBackgroud("white")
    ctx.restore();
    ctx.save();
    ctx.translate(x, 0);
    ctx.translate(0, 100);
    DrawWings("white");
    DrawEngines("white");
    DrawHead("white");
    DrawX("white");
    DrawBase("white");
    DrawLasers("red");
    
    //DrawDetails("grey")
    ///FuckingAround("green");
    ctx.restore();
    star_x += star_dir;
    star_y += star_dir;
    //star_y += star_dir;
    
    if (star_x > 20 || star_x < -20) {
        star_dir *= -1;
    }

    x = x + dir;
    if (x > 220 || x < -25) {
        dir *= -1;
    }
    y = y + 8;
    if (y > 400) {
        y = 20;
    }
    window.requestAnimationFrame(draw);
} 
const slider = document.getElementById("slider");
      
// Update the speed of the square based on the slider value

window.requestAnimationFrame(draw);




