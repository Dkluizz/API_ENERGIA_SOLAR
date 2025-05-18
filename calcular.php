<?php
// Recebe dados do formulário HTML
$data = [
    "consumo_kwh" => floatval($_POST['consumo_kwh']),
    "irradiancia" => floatval($_POST['irradiancia']),
    "eficiencia_placa" => floatval($_POST['eficiencia_placa']),
    "perdas" => floatval($_POST['perdas']),
    "potencia_placa_kw" => floatval($_POST['potencia_placa_kw']),
];

// Endpoint da sua API FastAPI
$url = "http://127.0.0.1:8000/consumo";

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data)); // Envia JSON
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']); // Informa tipo JSON
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

// Decodifica e exibe o resultado
$result = json_decode($response, true);

if ($result) {
    echo "<h1>Resultado do Cálculo:</h1>";
    echo "<p>Placas necessárias: <strong>" . round($result['placas_necessarias'], 2) . "</strong></p>";
    echo "<p>Potência total (kW): <strong>" . round($result['potencia_total_kw'], 2) . "</strong></p>";
    echo "<p>Observação: " . htmlspecialchars($result['observacao']) . "</p>";
} else {
    echo "<p>Erro ao calcular. Resposta inválida da API.</p>";
}
?>
