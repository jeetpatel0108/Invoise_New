function digitsOnly(input) {
    input.value = input.value.replace(/\D/g, "");
}

function lettersOnly(input) {
    input.value = input.value.replace(/[^a-zA-Z\s]/g, "");
}

function alphanumericSpace(input) {
    input.value = input.value.replace(/[^a-zA-Z0-9\s.\-&]/g, "");
}

function validateRegisterForm(form) {
    const phone = form.ph.value.replace(/\D/g, "");
    if (phone.length < 10 || phone.length > 12) {
        alert("Phone: enter 10–12 digits only (numbers). No letters.");
        form.ph.focus();
        return false;
    }
    if (!/^[a-zA-Z0-9_]{3,20}$/.test(form.u.value.trim())) {
        alert("Username: 3–20 characters, letters, numbers, underscore only.");
        form.u.focus();
        return false;
    }
    if (form.p.value.length < 6) {
        alert("Password: minimum 6 characters required.");
        form.p.focus();
        return false;
    }
    if (!/^[a-zA-Z\s]{2,50}$/.test(form.on.value.trim())) {
        alert("Owner name: letters only, no numbers.");
        form.on.focus();
        return false;
    }
    if (!/^[a-zA-Z\s]{2,50}$/.test(form.c.value.trim())) {
        alert("City: letters only, no numbers.");
        form.c.focus();
        return false;
    }
    if (form.a.value.trim().length < 5) {
        alert("Address: please enter full address (min 5 characters).");
        form.a.focus();
        return false;
    }
    form.ph.value = phone;
    return true;
}

function validateOtpForm(form) {
    const otp = form.otp.value.replace(/\D/g, "");
    if (otp.length !== 6) {
        alert("Enter 6-digit OTP (numbers only).");
        form.otp.focus();
        return false;
    }
    form.otp.value = otp;
    return true;
}
