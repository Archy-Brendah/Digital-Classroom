//show or hide edit form
$(function () {
    // run the currently selected effect
    function runEffect() {
        // get effect type from
        var selectedEffect = "fold";

        // Most effect types need no options passed by default
        var options = {};
        // some effects have required parameters
        if (selectedEffect === "scale") {
            options = {percent: 50};
        } else if (selectedEffect === "size") {
            options = {to: {width: 200, height: 60}};
        }

        // Run the effect
        $("#editForm").toggle(selectedEffect, options, 1500);
    }
    ;

    // Set effect from select menu value
    $("#edit").on("click", function () {
        runEffect();
    });
});