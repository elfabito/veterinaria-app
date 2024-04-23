document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
});

function edituser() {
  const user_id = JSON.parse(document.getElementById("user_id").textContent);
  const is_provedor = JSON.parse(
    document.getElementById("is_provedor").textContent
  );
  const regex_email =
    /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
  const regex_phone = /^\+[0-9]{1,3}[0-9]{4,14}(?:x+)?$/;
  let name = document.getElementById("fname");
  let apellido = document.getElementById("lname");
  let email = document.getElementById("email");
  let nameValue = name.innerHTML;
  let apellidoValue = apellido.innerHTML;
  let emailValue = email.innerHTML;
  let inputname = document.createElement("input");
  let inputapellido = document.createElement("input");
  let inputemail = document.createElement("input");
  inputname.value = nameValue;
  inputapellido.value = apellidoValue;
  inputemail.value = emailValue;
  name.innerHTML = "";
  apellido.innerHTML = "";
  email.innerHTML = "";
  name.append(inputname);
  apellido.append(inputapellido);
  email.append(inputemail);
  let btnDiv = document.getElementById("tbutton");
  let btnEdit = document.getElementById("buttonEdit");
  let button = document.createElement("button");
  button.className = "btn btn-secondary float-end";
  button.innerHTML = "Guardar";

  btnDiv.innerHTML = "";
  btnDiv.append(button);
  if (is_provedor) {
    let razonSocial = document.getElementById("razonsocial");
    let domicilio = document.getElementById("domicilio");
    let telefono = document.getElementById("telefono");
    let razonValue = razonSocial.innerHTML;
    let domicilioValue = domicilio.innerHTML;
    let telefonoValue = telefono.innerHTML;
    let inputdomicilio = document.createElement("input");
    let inputtelefono = document.createElement("input");
    let inputrazon = document.createElement("input");
    inputdomicilio.value = domicilioValue;
    inputtelefono.value = telefonoValue;
    inputrazon.value = razonValue;
    domicilio.innerHTML = "";
    razonSocial.innerHTML = "";
    telefono.innerHTML = "";
    telefono.append(inputtelefono);
    domicilio.append(inputdomicilio);
    razonSocial.append(inputrazon);
    button.addEventListener("click", (e) => {
      e.preventDefault();
      let name_new = inputname.value;
      let apellido_new = inputapellido.value;
      let domicilio_new = inputdomicilio.value;
      let telefono_new = inputtelefono.value;
      let email_new = inputemail.value;
      let razon_new = inputrazon.value;
      if (email_new.match(regex_email) && telefono_new.match(regex_phone)) {
        fetch(`/profile/${user_id}`, {
          method: "PUT",
          body: JSON.stringify({
            first_name: `${name_new}`,
            last_name: `${apellido_new}`,
            email: `${email_new}`,
            razonSocial: `${razon_new}`,
            domicilio: `${domicilio_new}`,
            telefono: `${telefono_new}`,
          }),
        }).then((result) => {
          location.href = "profile";
        });
      } else {
        alert("Ingresar un email / telefono valido. Ej +59899002030");
      }
      console.log(is_provedor);
    });
  } else {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      let name_new = inputname.value;
      let apellido_new = inputapellido.value;
      let email_new = inputemail.value;
      console.log(is_provedor);

      fetch(`/profile/${user_id}`, {
        method: "PUT",
        body: JSON.stringify({
          first_name: `${name_new}`,
          last_name: `${apellido_new}`,
          email: `${email_new}`,
        }),
      }).then((result) => {
        // value = content_new;
        // btn.innerHTML = "";
        // btn.append(btnEdit);
        // element.innerHTML = value;
        // document.getElementById("data").innerHTML = "";
        location.href = "profile";
      });
    });
  }
}

function reservac(doctor, dayOfWeek) {
  selected = document.getElementById(
    `${doctor.first_name} ${siguienteFecha(dayOfWeek)}`
  );
  value = selected.value;
  fecha = siguienteFecha(dayOfWeek);

  // Format date to datetimefield , i recieve (DAY / MONTH / YEAR )

  date = fecha.split("/");
  dateeng = date.reverse().join("-");
  time = value.split(":");
  datetime = dateeng + " " + time[0] + ":00";

  var comment = document.getElementById("id_comment");

  fetch(`reserva`, {
    method: "POST",
    body: JSON.stringify({
      service: doctor.position,
      doctor: doctor,
      datetime: datetime,
      comment: comment.value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (
        result["msg"] == "Reserva realizada con exito, espere a ser aprobado."
      ) {
        location.href = "profile";
      } else {
        window.location.reload();
      }
    });
}

function approved(id) {
  fetch(`reserva/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      canceled: false,
      approved: true,
    }),
  }).then((result) => {
    window.location.reload();
  });
}

function cancelAppoint(id) {
  fetch(`reserva/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      canceled: true,
      approved: false,
    }),
  }).then((result) => {
    window.location.reload();
  });
}

function deleteAppoint(id) {
  fetch(`reserva/${id}`, {
    method: "DELETE",
  })
    .then((response) => response.json()) // or res.json()
    .then((result) => window.location.reload());
}
