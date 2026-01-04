<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PayloadController;

Route::post('/payloads', [PayloadController::class, 'store']);
Route::get('/payloads/{id}', [PayloadController::class, 'show']);
Route::put('/payloads/{id}', [PayloadController::class, 'update']);
Route::delete('/payloads/{id}', [PayloadController::class, 'destroy']);
Route::post('/payloads/{id}/pay', [PayloadController::class, 'pay']);