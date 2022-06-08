<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

use Illuminate\Support\Facades\DB;

class WayPointSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('waypoints')->insert([
            'index' => 0,
            'wandelroute_id' => 1,
            'latitude' => 59.91399190713849, 
            'longitude' => 10.752465239770952
        ]);
        DB::table('waypoints')->insert([
            'index' => 1,
            'wandelroute_id' => 1,
            'latitude' => 59.915179790103934,
            'longitude' => 10.751629792858958
        ]);
}
}
