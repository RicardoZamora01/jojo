import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Header from "../components/Header";
import "../styles/test.css"

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

function Home() {

  const [charactersList, setCharactersList] = useState<Character[]>([]);

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
          console.log("characterList:", characterList);
        } else {
          console.error("No characters found in the data.");
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div className="">
      <Navbar/>
      <Header/>
      
        <h1 id="all-stands" className="text-5xl font-bold">Jojo's Bizarre Adventure</h1>
        <div>
          {charactersList.map((character, index) => (
            <div key={index}>
              <h2>{character.name}</h2>
              <p className="">
                Stand Names:{" "}
                {character.standNames ? character.standNames.join(", ") : ""}
              </p>
              <div>
                Stand Attributes:
                <ul>
                  {character.standAttributes ? (
                    character.standAttributes.map((attribute, index) => (
                      <li key={index}>
                        <strong>{attribute.stand_power},</strong>{" "}
                        {attribute.stand_speed}, {attribute.stand_range},{" "}
                        {attribute.stand_durability},{" "}
                        {attribute.stand_precision},{" "}
                        {attribute.stand_development_potential}
                      </li>
                    ))
                  ) : (
                    <li>No Stand Attributes</li>
                  )}
                </ul>
              </div>
            </div>
          ))}
        </div>
    </div>

    // <div>
    //   <h1>Welcome to the Home Page</h1>
    //   {/* Content specific to the home page */}
    // </div>
  );
}

export default Home;
