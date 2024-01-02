import { useEffect, useState } from "react";
import tbd from "../assets/tbd.png";
import Header from "../components/Header";
import Navbar from "../components/Navbar";
import "../styles/test.css";

interface Character {
  name: string;
  standNames: string[] | undefined;
  standAttributes: StandAttribute[] | undefined; // Add undefined to the type
}

interface StandAttribute {
  stand_power: string;
  stand_speed: string;
  stand_range: string;
  stand_durability: string;
  stand_precision: string;
  stand_development_potential: string;
}

interface Stand {
  name: string;
  stand_power: string;
  stand_speed: string;
  stand_range: string;
  stand_durability: string;
  stand_precision: string;
  stand_development_potential: string;
}

interface CompleteCharacter {
  name: string;
  stands: Stand[];
}

function Home() {
  const [charactersList, setCharactersList] = useState<Character[]>([]);
  const [fullCharacterList, setFullCharacterList] = useState<
    CompleteCharacter[]
  >([]);

  useEffect(() => {
    fetch("/characters")
      .then((res) => res.json())
      .then((data) => {
        console.log("API Response:", data);
        if (Array.isArray(data) && data.length > 0) {
          const characterList = data.map((character) => ({
            name: character[0],
            standNames: character[1],
            standAttributes: character[2],
          }));

          setCharactersList(characterList);
        } else {
          console.error("No characters found in the data.");
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);



  useEffect(() => {
    const updatedFullCharacterList = charactersList.map((character) => {
      const stands = character.standAttributes?.map((stand) => ({
        name: character.standNames?.[character.standAttributes?.indexOf(stand) || 0] || "",
        stand_power: stand.stand_power || "",
        stand_speed: stand.stand_speed || "",
        stand_range: stand.stand_range || "",
        stand_durability: stand.stand_durability || "",
        stand_precision: stand.stand_precision || "",
        stand_development_potential: stand.stand_development_potential || "",
      }));

      return {
        name: character.name,
        stands: stands || [],
      };
    });

    setFullCharacterList(updatedFullCharacterList);
  }, [charactersList]);

  return (
    <div className="">
      <Navbar />
      <Header />

      <h1
        id="all-stands"
        className="flex justify-center text-5xl font-bold pt-6"
      >
        Character Stand Showcase
      </h1>

      {fullCharacterList.map((character, index) => (
        <div className="border-solid border-indigo-900 border-8 m-12 rounded-2xl"key={index}>
          <h2 className="text-3xl font-bold px-12 pt-6">{character.name}</h2>
          <div>
            {character.stands.map((stand, index) => (
              <div key={index}>
                <div className="flex flex-row justify-between border-solid border-indigo-900 border-2 mx-12 my-8 rounded-lg">
                  <div>
                    <h3 className="text-2xl font-bold px-8 pt-6">{stand.name}</h3>
                    <div className="flex flex-col px-12">
                      <div className="flex flex-col">
                        <p className="font-bold">Stand Power</p>
                        <p>{stand.stand_power}</p>
                      </div>
                      <div className="flex flex-col">
                        <p className="font-bold">Stand Speed</p>
                        <p>{stand.stand_speed}</p>
                      </div>
                      <div className="flex flex-col">
                        <p className="font-bold">Stand Range</p>
                        <p>{stand.stand_range}</p>
                      </div>
                      <div className="flex flex-col">
                        <p className="font-bold">Stand Durability</p>
                        <p>{stand.stand_durability}</p>
                      </div>
                      <div className="flex flex-col">
                        <p className="font-bold">Stand Precision</p>
                        <p>{stand.stand_precision}</p>
                      </div>
                      <div className="flex flex-col">
                        <p className="font-bold">Stand Development Potential</p>
                        <p>{stand.stand_development_potential}</p>
                      </div>
                    </div>
                  </div>
                  <img src={tbd} alt="tbd" className="max-w-xs mx-12 pt-6" />
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
export default Home;
