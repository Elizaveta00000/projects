<?php

namespace App\Http\Controllers;                                 //главный контроллер
use App\m_Event;
use App\m_Participant;
use App\User;
use Illuminate\Support\Facades\Cache;
use Illuminate\Database\Eloquent;
use App\m_Person;
use App\m_Buffer;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;


class IndexController extends Controller
{

    public function main()
    {
        $dop = User::query()->exists();
        return view('index_copy', compact('dop'));

    }

    public function index()
    {                                           // ВЫВОД СОДЕРЖИМОГО ТАБЛИЦЫ
        $bufferPerson = m_Buffer::all();
        return view('index_search', compact('bufferPerson'));
    }

    protected $s;

    public function search(Request $request)
    {           //функция для поиска данных по таблице
        $s = $request->s;
        Cache::put('find', "{$s}");             //НЕ ТРОГАТЬ!!! кладу в стэк значение для поиска для дальнейшего экспорта

        $bufferPerson = m_Buffer::query()->where('Surname', 'LIKE', "%{$s}%")
            ->orWhere('year_of_admission', 'LIKE', "%{$s}%")
            ->orWhere('ev_name', 'LIKE', "%{$s}%")
            ->orWhere('subject', 'LIKE', "%{$s}%")
            ->orWhere('date', 'LIKE', "%{$s}%")
            ->get();

        return view('search_COPY', compact('bufferPerson'));
    }

    public function person()
    {
        $persInfo = m_Person::all();
        return view('personalInformation', compact('persInfo'));
    }

    public function relocation()
    {

        $bufferPerson = DB::select('select distinct *
        from BufferPersonEvent as b
        where not exists (select Surname, Name, Patronymic, birthDay, city, locality, tel, email,
        class, year_of_admission from Persons
        where Surname = b.Surname and Name=b.Name and (Patronymic=b.Patronymic or (b.Patronymic is null or Patronymic is null))
        and birthDay=b.birthDay)');

        if (count($bufferPerson)) {
            foreach ($bufferPerson as $buf) {
                $person = new m_Person();
                $person->Surname = $buf->Surname;
                $person->Name = $buf->Name;
                $person->Patronymic = $buf->Patronymic;
                $person->birthDay = $buf->birthDay;
                $person->citizenship = $buf->citizenship;
                $person->tel = $buf->tel;
                $person->email = $buf->email;
                $person->country = $buf->country;
                $person->region = $buf->region;
                $person->city = $buf->city;
                $person->locality = $buf->locality;
                $person->street = $buf->street;
                $person->house = $buf->house;
                $person->building = $buf->building;
                $person->apartment = $buf->apartment;
                $person->class = $buf->class;
                $person->year_of_admission = $buf->year_of_admission;
                $person->save();
            }
        }
    }
}
