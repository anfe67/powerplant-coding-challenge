 $(document).ready(function() {

            logNamespace = '/log';    // logging events
            var logSocket = io(logNamespace);
            console.log('Connection attempted...')

            logSocket.on('welcome', function(msg) {
                 var title = document.getElementById("ppTitle");
                 title.innerHTML = '<h1>' + msg + '</h1>';

            });     

            logSocket.on('request_processed', function(msg) {
                  // Locate container
                  previous = document.getElementById("allocationRequests").innerHTML;

                  // Append HTML
                  document.getElementById("allocationRequests").innerHTML = previous + "<hr>" + msg;
                  window.scrollTo(0,document.body.scrollHeight);
            });

});