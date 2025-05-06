document.addEventListener("DOMContentLoaded", function () {
  const subscribeForm = document.getElementById("footerSubscribeForm");
  const emailInput = document.getElementById("footerEmail");
  const subscribeButton = document.getElementById("footerSubscribeButton");
  const loadingSpinner = document.getElementById("footerLoadingSpinner");
  const successMessage = document.getElementById("subscribeSuccessMessage");
  const errorMessage = document.getElementById("subscribeErrorMessage");

  // Email validation regex
  const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  if (subscribeForm) {
    subscribeForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      // Reset messages
      hideMessages();

      const email = emailInput.value.trim();

      // Client-side validation
      if (!email || !EMAIL_REGEX.test(email)) {
        showError("Please enter a valid email address.");
        return;
      }

      // Show loading state
      subscribeButton.disabled = true;
      loadingSpinner.style.display = "inline-block";

      try {
        // TODO: Replace with your Supabase function URL
        const response = await fetch(
          "https://eaqibtmhonekgkzkuitp.supabase.co/functions/v1/email_subscriptions",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email }),
          }
        );

        const data = await response.json();

        if (response.ok) {
          // Success
          showSuccess(data.message || "Thank you for subscribing!");
          subscribeForm.reset();
        } else {
          // API error
          showError(data.error || "Something went wrong. Please try again.");
        }
      } catch (error) {
        // Network or other error
        showError(
          "Connection error. Please check your internet and try again."
        );
        console.error("Subscription error:", error);
      } finally {
        // Reset loading state
        subscribeButton.disabled = false;
        loadingSpinner.style.display = "none";
      }
    });
  }

  function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.style.display = "block";
    setTimeout(() => {
      successMessage.style.display = "none";
    }, 10000); // Increased from 5000 to 10000 (10 seconds)
  }

  function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = "block";
    setTimeout(() => {
      errorMessage.style.display = "none";
    }, 10000); // Increased from 5000 to 10000 (10 seconds)
  }

  function hideMessages() {
    successMessage.style.display = "none";
    errorMessage.style.display = "none";
  }
});
