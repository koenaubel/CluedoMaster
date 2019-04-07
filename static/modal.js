function submitSugg() {
//    clickEvent.preventDefault();
    turnPlayerName = $("[name=turn_player]").val();
    $("#suggestion").hide();
    $("#showCard").show();
    $('option[id="' + turnPlayerName + '"]').hide();
}