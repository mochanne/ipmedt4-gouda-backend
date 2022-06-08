<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class WandelRoute extends Model
{
    protected $table = "wandelroutes";

    public function waypoints() {
        return $this->hasMany(WayPoint::class, 'wandelroute_id', 'id')->orderBy("index");
    }
    public function infopoints() {
        return $this->hasMany(InfoPoint::class, 'wandelroute_id', 'id')->orderBy("index");
    }

}
