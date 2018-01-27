
function showErrorModal(message) {
    modal = $("#errorModal");
    modal.find('.modal-body').text(message);
    modal.modal('show');
}

function windowScrollTo(elementId) {
    document.getElementById(elementId).scrollIntoView({
        block: 'start',
        behavior: 'smooth',
    });
}
