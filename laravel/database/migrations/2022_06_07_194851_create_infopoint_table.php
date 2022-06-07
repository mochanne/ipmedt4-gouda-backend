<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('infopoints', function (Blueprint $table) {
            $table->id();
            $table->integer("index"); // volgorde in verhouding met andere punten. gebruikt voor sorteren
            $table->foreignId("wandelroute_id")->constrained();
            $table->string("naam", 128)->nullable(); // naam van het punt
            $table->string("afbeelding",255);
            $table->point("positie"); // long/las positie
            $table->text("gedicht");
            $table->text("info")->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('infopoint');
    }
};
