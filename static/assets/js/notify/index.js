'use strict';
var notify = $.notify('<i style="font-size:25px" class="bi bi-reception-4"></i><strong>Loading</strong> Data Retrieval ...', {
    type: 'theme',
    allow_dismiss: true,
    delay: 2000,
    showProgressbar: true,
    timer: 300
});

setTimeout(function() {
    notify.update('message', '<i style="font-size:25px" class="bi bi-wifi"></i><strong>Loading</strong> sytem Data...');
}, 1000);
