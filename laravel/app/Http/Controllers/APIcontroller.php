<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class APIcontroller extends Controller
{
    public function GetRouteList()
    {
        $out = \App\Models\WandelRoute::all();
        foreach ($out as $route) {
            $route->afbeelding = $route->infopoints()->first()->afbeelding();
            $route->aantal = $route->infopoints()->count();
        }
        return $out;
    }

    public function GetRouteInfo($route_id)
    {
        $route = \App\Models\WandelRoute::find($route_id);

        foreach ($route->infopoints as $infopoint) {
            $infopoint->afbeelding = $infopoint->afbeelding();
            //echo $infopoint->afbeelding;
        }
        
        $route->afbeelding = $route->infopoints()->first()->afbeelding();
        $route->aantal = $route->infopoints()->count();

        $route->waypoints;


        // $route->infopoints->sortBy("index");
        // $route->waypoints->sortBy("index");

        return $route;
    }
}
