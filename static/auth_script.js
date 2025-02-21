document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", (e) => {
        // Campos do formulário
        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");

        // Valores dos campos
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        // Limpar mensagens anteriores
        document.querySelectorAll(".invalid-feedback").forEach((el) => el.remove());
        usernameInput.classList.remove("is-invalid");
        passwordInput.classList.remove("is-invalid");

        let hasError = false;

        // Validação do campo username
        if (!username) {
            const error = document.createElement("div");
            error.className = "invalid-feedback";
            error.textContent = "O campo Usuário é obrigatório.";
            usernameInput.classList.add("is-invalid");
            usernameInput.insertAdjacentElement("afterend", error);
            hasError = true;
        }

        // Validação do campo password
        if (!password) {
            const error = document.createElement("div");
            error.className = "invalid-feedback";
            error.textContent = "O campo Senha é obrigatório.";
            passwordInput.classList.add("is-invalid");
            passwordInput.insertAdjacentElement("afterend", error);
            hasError = true;
        }

        // Impedir envio do formulário se houver erros
        if (hasError) {
            e.preventDefault();
        }
    });
});
