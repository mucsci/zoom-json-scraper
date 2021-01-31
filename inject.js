$('td.col6[data-column="table.p"]').each((i,e) => {
    const anchor = $(e).children();
    const meetingId = encodeURIComponent(anchor.attr("data-id"));
    const userId = encodeURIComponent(anchor.attr("data-accountid"));
    const newLink = $('<a>');
    newLink.attr("href","https://millersville.zoom.us/account/my/report/participants/list?meetingId=" + meetingId + "&accountId=" + userId);
    newLink.attr("target","_blank");
    newLink.text("JSON");
    $(e).append(newLink);
  });
  