<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Storage;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\URL;

class AutoDBSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $index = 0;
        foreach(Storage::disk('wandelroutes')->directories() as $item) { 
            $index += 1;
            echo $index;
            echo ": ";
            echo $item;

            DB::table('wandelroutes')->insert([
                'naam' => $item,
                'id' => $index,
            ]);

            foreach (Storage::disk('wandelroutes')->directories($item) as $IP_dir) {
                $IP_index = explode('$',str_replace($item . '/', '',$IP_dir))[0];
                $json = json_decode(Storage::disk('wandelroutes')->get($IP_dir . '/data.json'), true);
                echo $IP_dir;
                DB::table('infopoints')->insert([
                    'index' => $IP_index,
                    'wandelroute_id' => $index,
                    'naam' => $json['titel'],
                    'gedicht' => $json['gedicht'],
                    'latitude' => $json['latitude'] ?? 0.0,
                    'longitude' => $json['longitude'] ?? 0.0,
                    'afbeelding' => URL::to('/storage/wandelroutes/' . $IP_dir . '/img.jpeg')
                ]);
            }
        }
    }
}
