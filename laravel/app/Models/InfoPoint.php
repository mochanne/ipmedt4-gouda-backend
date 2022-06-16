<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

use Illuminate\Support\Facades\URL;

class InfoPoint extends Model
{
    protected $table = "infopoints";

    //$this->afbeelding = URL::to($this->afbeelding);

    public function afbeelding()
    {
	return URL::to($this->afbeelding);
    }

}
