<?php if (!defined('PmWiki')) exit();
$WikiTitle = "Wiki";
$PageLogoUrl = "../";

$DefaultPasswords['admin'] = pmcrypt('onesecret');

$EnableUpload = 1;
$DefaultPasswords['upload'] = pmcrypt('secrettwo');

# Uncomment and change these if needed
# putenv("TZ=EST5EDT"); # if you run PHP 5.0 or older
# date_default_timezone_set('America/New_York'); # if you run PHP 5.1 or newer

$TimeFmt = '%B %d, %Y, at %I:%M %p EST';
include_once($FarmD.'/cookbook/displayhtml.php');
