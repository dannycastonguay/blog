// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

// Import required dependencies
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { v4 as uuidv4 } from "https://esm.sh/uuid@9.0.0";

// Define the email subscriber interface
interface EmailSubscriber {
  email: string;
  active?: boolean;
  id?: string;
}

// Email validation regex
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

serve(async (req) => {
  // CORS headers to allow requests from any origin
  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers":
      "authorization, x-client-info, apikey, content-type",
    "Content-Type": "application/json",
  };

  // Handle OPTIONS request for CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: corsHeaders,
    });
  }

  // Get the URL path
  const url = new URL(req.url);
  const path = url.pathname.split("/").pop();

  // Handle unsubscribe requests
  if (path === "unsubscribe" && req.method === "GET") {
    const id = url.searchParams.get("id");

    if (!id) {
      return new Response(JSON.stringify({ error: "Missing ID parameter" }), {
        status: 400,
        headers: corsHeaders,
      });
    }

    try {
      // Create a Supabase client
      const supabaseClient = createClient(
        Deno.env.get("SUPABASE_URL") ?? "",
        Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
      );

      // Delete the subscriber record
      const { error } = await supabaseClient
        .from("email_subscribers")
        .delete()
        .eq("id", id);

      if (error) {
        console.error("Error unsubscribing:", error);
        return new Response(
          JSON.stringify({
            error: "Failed to unsubscribe. Please try again later.",
          }),
          { status: 500, headers: corsHeaders }
        );
      }

      // Return success response as JSON
      return new Response(
        JSON.stringify({
          success: true,
          message: "Successfully unsubscribed from the newsletter.",
        }),
        { status: 200, headers: corsHeaders }
      );
    } catch (error) {
      console.error("Unexpected error:", error);
      return new Response(
        JSON.stringify({
          error: "An unexpected error occurred. Please try again later.",
        }),
        { status: 500, headers: corsHeaders }
      );
    }
  }

  // Handle POST requests for subscription
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: corsHeaders,
    });
  }

  try {
    // Parse the request body
    const { email } = await req.json();

    // Validate email
    if (!email || typeof email !== "string" || !EMAIL_REGEX.test(email)) {
      return new Response(JSON.stringify({ error: "Invalid email address" }), {
        status: 400,
        headers: corsHeaders,
      });
    }

    // Create a Supabase client with the project URL and service role key to bypass RLS
    const supabaseClient = createClient(
      // Supabase API URL - env var exported by default when deployed
      Deno.env.get("SUPABASE_URL") ?? "",
      // Supabase SERVICE ROLE KEY - env var exported by default when deployed
      // Using service role key to bypass RLS policies
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    // Check if the email already exists
    const { data: existingSubscriber } = await supabaseClient
      .from("email_subscribers")
      .select("email")
      .eq("email", email.toLowerCase().trim())
      .maybeSingle();

    if (existingSubscriber) {
      // Email already exists, return a friendly message
      return new Response(
        JSON.stringify({
          success: true,
          message: "You're already subscribed!",
        }),
        { status: 200, headers: corsHeaders }
      );
    }

    // Prepare the subscriber data
    const subscriber: EmailSubscriber = {
      email: email.toLowerCase().trim(),
      active: true,
    };

    // Insert the subscriber into the database
    const { error } = await supabaseClient
      .from("email_subscribers")
      .insert(subscriber);

    if (error) {
      console.error("Error inserting subscriber:", error);

      // Log the actual error for debugging but don't return it to the client
      return new Response(
        JSON.stringify({
          error: "Failed to add subscriber. Please try again later.",
        }),
        { status: 500, headers: corsHeaders }
      );
    }

    // Return success response
    return new Response(
      JSON.stringify({
        success: true,
        message: "Subscription successful! Thank you for subscribing.",
      }),
      { status: 200, headers: corsHeaders }
    );
  } catch (error) {
    // Log the actual error for debugging
    console.error("Unexpected error:", error);

    // Return a generic error message to the client
    return new Response(
      JSON.stringify({
        error: "An unexpected error occurred. Please try again later.",
      }),
      { status: 500, headers: corsHeaders }
    );
  }
});

/* To invoke locally:

  1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
  2. Make an HTTP request:

  curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/email_subscriptions' \
    --header 'Content-Type: application/json' \
    --data '{"email":"example@example.com"}'

*/
