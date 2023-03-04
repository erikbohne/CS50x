document.addEventListener('DOMContentLoaded', function() {

    // If the fact-buttons are clicked the answere to that fact will appear underneath.
    document.getElementById('q1').addEventListener('click', function() {
        document.querySelector('#fact1').innerHTML = 'Dancing Queen - Abba';
    });

    document.getElementById('q2').addEventListener('click', function() {
        document.querySelector('#fact2').innerHTML = 'Interstellar';
    });

    document.getElementById('q3').addEventListener('click', function() {
        document.querySelector('#fact3').innerHTML = 'Bergen, Norway';
    });

    document.getElementById('q4').addEventListener('click', function() {
        document.querySelector('#fact4').innerHTML = '234km (7.5 hours)';
    });

    // If "next is clicked the next image in the library will appear
    let number = 1
    document.getElementById('next').addEventListener('click', function() {
        if (number == 10) {
            number = 1;
        }
        else {
            number += 1;
        }
        document.querySelector('#img').src = (`images/${number}.jpg`)
    });

    // If "previous" is clicked the previous image in the library wil appear
    document.getElementById('previous').addEventListener('click', function() {
        if (number == 1) {
            number = 10;
        }
        else {
            number -= 1;
        }
        document.querySelector('#img').src = (`images/${number}.jpg`)
    });
});