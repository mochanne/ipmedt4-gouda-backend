<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class APIcontroller extends Controller
{
    public function GetRouteList()
    {
        return \App\Models\WandelRoute::all();
    }

    public function GetRouteInfo($route_id)
    {
        $route = \App\Models\WandelRoute::find($route_id);

        $route->infopoints;
        $route->waypoints;


        // $route->infopoints->sortBy("index");
        // $route->waypoints->sortBy("index");

        return $route;
    }
}
