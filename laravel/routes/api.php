<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::get('ping', function () {
    return 'pong';
});

Route::get('routelist', [\App\Http\Controllers\APIcontroller::class, 'GetRouteList']);

Route::get('routeinfo/{route_id}', [\App\Http\Controllers\APIcontroller::class, 'GetRouteInfo']);