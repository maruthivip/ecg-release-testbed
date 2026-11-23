<?php

use App\Http\Controllers\OrderController;
use Illuminate\Support\Facades\Route;

Route::get('/release/orders/{id}', [OrderController::class, 'show']);
