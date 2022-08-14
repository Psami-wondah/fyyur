window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

button = document.getElementById("delete-venue-button");
button.onclick = function (e) {
  console.log("event", e);
  const venueId = e.target.dataset.id;
  fetch("/venues/" + venueId, {
    method: "DELETE",
  })
    .then((res) => {
      console.log(res);
      document.location.href = "/";
    })
    .catch(function () {
      console.error(err);
    });
};
