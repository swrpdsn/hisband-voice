// Supabase Configuration
// In a real production environment, these should be loaded from environment variables
// on the server, not exposed directly in client-side JavaScript.
// For this static HTML MVP, we will keep them here, but it's a known security tradeoff.

const SUPABASE_URL = 'https://hsrkrjfcaevsseldoddt.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhzcmtyamZjYWV2c3NlbGRvZGR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNzQxMzksImV4cCI6MjA3NDY1MDEzOX0.c44_PL8XF3B6mSoJSx4QLknoAno89mcIyw0miGdMb9Y';

window.supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);