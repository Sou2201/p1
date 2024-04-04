$(document).ready(function() {
   
    function fetchEvents() {
        $.ajax({
            url: '/events',
            type: 'GET',
            success: function(data) {
                displayEvents(data);
            },
            error: function(error) {
                console.error('Error fetching events:', error);
            }
        });
    }

    
    function displayEvents(events) {
        $('#events-container').empty();
        events.forEach(function(event) {
            $('#events-container').append('<p>' + event + '</p>');
        });
    }

    
    fetchEvents();

    
    setInterval(fetchEvents, 15000);
});
