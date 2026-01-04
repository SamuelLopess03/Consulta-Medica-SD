<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Payload extends Model
{
    protected $fillable = [
        'agendamento_id',
        'total',
        'status',
        'payment_method',
        'customer_email',
    ];
}
