<?php

$public_key = "qBvJaMi0QcLmxMX5wiab2kuJxFSOi2cU8LvxTVZn";
$secret_key = "pXGToH2CFBPkDBF1sPXpG74UabUB8TEUfK98zYal";

$api_path = "/v3/auth/kuna_codes/issued-by-me";
$nonce = strval(date_timestamp_get(date_create()));
$body = (object) array();

$signatureString =  $api_path.$nonce.json_encode($body); 

$signature = hash_hmac("sha384", $signatureString, $secret_key);
printf($signature); // выводит подпись в HEX формате
?>