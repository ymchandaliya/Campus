var ignoreClickOnMeElement = document.getElementById('inputEnroll');

document.addEventListener('click', function(event) {
    var isClickInsideElement = ignoreClickOnMeElement.contains(event.target);
    if (!isClickInsideElement) {

        //Do something click is outside specified element
        const request = new XMLHttpRequest();
        //  const currency = document.querySelector('#currency').value;
        request.open('POST', 'signup');
         // Callback function for when request completes
         request.onload = () => {
             // Extract JSON data from request
             const data = JSON.parse(request.responseText);
             // Update the result div
             if (data.success) {
               const contents = `1 USD is equal to.`
               document.querySelector('#Error').innerHTML = contents;
             }
             else {
               document.querySelector('#Error').innerHTML = 'There was an error.';
             }
           }
         // Add data to send with request
         const data = new FormData();
         data.append('inputEnroll', inputEnroll);
         // Send request
         request.send(data);
         return false;
        // document.getElementById("Error").innerHTML = "New text!";


    }
});
