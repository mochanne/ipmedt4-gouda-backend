<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

use Illuminate\Support\Facades\DB;

class InfoPointSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('infopoints')->insert([
            'index' => 0,
            'wandelroute_id' => 1,
            'naam' => 'gamer straat',
            'gedicht' => 'hoi',
            'latitude' => 1.0,
            'longitude' => 1.0,
            'afbeelding' => 'https://upload.wikimedia.org/wikipedia/en/9/9a/Among_Us_cover_art.jpg',
        ]);
    }
}
