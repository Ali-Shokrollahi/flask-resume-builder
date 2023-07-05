$(function () {
    var CurrentUrl = document.URL;
    var CurrentUrlEnd = CurrentUrl.split('/').filter(Boolean).pop();

    $(".dashboard__item a").each(function () {
        var ThisUrl = $(this).attr('href');
        var ThisUrlEnd = ThisUrl.split('/').filter(Boolean).pop();

        if (ThisUrlEnd == CurrentUrlEnd)
            $(this).parent().addClass('active')
    });
});

function add_job(elem) {
    var adddiv = document.querySelector(".add-job")
    if (elem.firstChild.className == "fa fa-plus") {
        adddiv.classList.add("d-block")
        elem.firstChild.className = "fa fa-minus"
    } else {
        adddiv.classList.remove("d-block")
        elem.firstChild.className = "fa fa-plus"
    }
}


function delete_edu(edu_id) {
    if (confirm('آیا از حذف این مورد اطمینان دارید؟')) {
        $.post("/dashboard/educations/delete",
            {
                id: edu_id
            }, function (response) {
                $('#education-' + edu_id).remove();

            }
        )
    }


}

function delete_exp(exp_id) {
    if (confirm('آیا از حذف این مورد اطمینان دارید؟')) {
        $.post("/dashboard/experiences/delete",
            {
                id: exp_id
            }, function (response) {
                $('#experience-' + exp_id).remove();

            }
        )
    }


}

function delete_skill(skill_id) {
    if (confirm('آیا از حذف این مورد اطمینان دارید؟')) {
        $.post("/dashboard/skills/delete",
            {
                id: skill_id
            }, function (response) {
                $('#skill-' + skill_id).remove();

            }
        )
    }


}

function delete_por(portfolio_id) {
    if (confirm('آیا از حذف این مورد اطمینان دارید؟')) {
        $.post("/dashboard/portfolios/delete",
            {
                id: portfolio_id
            }, function (response) {
                $('#portfolio-' + portfolio_id).remove();

            }
        )
    }


}

function showpic(elem) {

    $(elem).parent().find("#file").trigger("click")
}