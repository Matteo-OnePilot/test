import * as http from 'http';

// 1. Secret en dur (Sera détecté par p/secrets)
const STRIP_SECRET_KEY = "sk_live_1234567890abcdef1234567890abcdef";
const DB_PASSWORD = "super_secret_admin_password_123!";

function processData(userInput: string) {
    // 2. Utilisation dangereuse de eval() (Sera détecté par p/default)
    const result = eval(userInput);
    console.log(result);
}

// 3. Vulnérabilité XSS (Cross-Site Scripting)
http.createServer((req, res) => {
    const url = new URL(req.url || '', `http://${req.headers.host}`);
    // Récupération d'un paramètre non sécurisé depuis l'URL
    const userName = url.searchParams.get('name') || 'Visiteur';

    res.writeHead(200, { 'Content-Type': 'text/html' });
    // DANGER : Injection directe de l'entrée utilisateur dans le HTML
    res.write(`<h1>Bienvenue, ${userName}</h1>`); 
    res.end();
}).listen(8080);
