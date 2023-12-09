$(document).ready(function () {
    // 点击刷新按钮时获取招新信息
    $("#refreshRecruitmentBtn").click(function () {
        var url = "{% url 'api.get_recrus' %}";  // 替换为你的刷新视图的 URL
        $.ajax({
            url: url,
            type: 'get',
            success: function (data) {
                var content = ''
                data.forEach(function (item) {
                    content += '<h3>' + item.title + '</h3>';
                    content += '<p>' + item.content + '</p>';
                });
                $("#recruitmentList").append(content);
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });

    $("#refreshLabBtn").click(function () {
        var url = $(this).data("url");  // 替换为你的刷新视图的 URL
        $.ajax({
            url: url,
            type: 'get',
            success: function (data) {
                var content = ''
                data.forEach(function (item) {
                    content += '<h3>' + item.name + '</h3>';
                    content += '<p>' + item.description + '</p>';
                });
                $("#LabList").append(content);
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });

    $(".tab-link").click(function() {
        var url = $(this).data("url");
        var clickedTab = $(this).attr("href");
        var target = $(clickedTab);
        var tabContent = target.find("[data-name='content']")
        var tabId = target.attr("id");

        $.ajax({
            url: url,
            type: 'get',
            success: function (data) {
                var content = '';
                if (tabId === "recruInfo") {
                    data.forEach(function (item) {
                        content += '<tr>';
                        content += '<td>' + item.title + '</td>';
                        content += '<td>' + item.content + '</td>';
                        content += '<td>' + item.lab_name + '</td>';
                        content += '</tr>';
                    });
                }
                else if (tabId === "labInfo") {
                    data.forEach(function (item) {
                        content += '<tr>';
                        content += '<td>' + item.name + '</td>';
                        content += '<td>' + item.description + '</td>';
                        content += '</tr>';
                    });
                }
                else if (tabId === "labAdmin") {
                    data.forEach(function (item) {
                        content += '<tr>';
                        content += '<td>' + item.name + '</td>';
                        content += '</tr>';
                    });
                }
                else if (tabId === "myApply") {
                    data.forEach(function (item) {
                        content += '<tr>';
                        content += '<td>' +
                            '<a href="{% url \'main.index\' %}" class="btn btn-primary">查看</a>' +
                            '</td>';
                        content += '<td>' + item.lab_name + '<td>';
                        content += '<td>' + item.status + '</td>';
                        content += '</tr>';
                    });
                }
                tabContent.append(content);
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});