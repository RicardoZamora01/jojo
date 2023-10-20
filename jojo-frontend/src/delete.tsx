function Delete() {
  // useEffect(() => {
  //   fetch('/characters')
  //     .then((res) => res.json())
  //     .then((data) => {
  //       console.log('API Response:', data);
  //       if (Array.isArray(data) && data.length > 0) {
  //         data.map((character) => {
  //           console.log('character:', character)

  //           const characterObj: Character = {
  //             name: character[0],
  //             standNames: character[1],
  //             standAttributes: character[2],
  //           }

  //           setCharactersList((prevCharactersList) => [...prevCharactersList, characterObj])

  //           // setCharacters({
  //           //   name: character[0],
  //           //   standNames: character[1],
  //           //   standAttributes: character[2],
  //           // });

  //           // setCharactersList((prevCharactersList) => [...prevCharactersList, characters])
  //         })
  //         // setCharacters({
  //         //   name: data[0][0],
  //         //   standNames: data[0][1],
  //         //   standAttributes: data[0][2],
  //         // });
  //         // console.log('character name:', data[0][0])
  //         // console.log('stand names:', data[0][1])
  //         // console.log('stand attributes:', data[0][2])
  //       }
  //       else {
  //         setCharacters({
  //           name: data[0][0],
  //           standNames: data[0][1],
  //           standAttributes: data[0][2],
  //         });
  //         setCharactersList([characters])
  //       }
  //       console.log('charactersList:', charactersList)
  //     })
  //     .catch((error) => {
  //       console.error('Error fetching data:', error);
  //     });
  // }, []);

  
    /* <p>Name: {characters.name}</p>
        <p>Stand Names: {characters.standNames ? characters.standNames.join(', ') : ''}</p>
        <div>
          Stand Attributes:
          <ul>
            {characters.standAttributes ? (
              characters.standAttributes.map((attribute, index) => (
                <li key={index}>
                  <strong>{attribute.stand_power},</strong> {attribute.stand_speed},{' '}
                  {attribute.stand_range}, {attribute.stand_durability},{' '}
                  {attribute.stand_precision}, {attribute.stand_development_potential}
                </li>
              ))
            ) : (
              <li>No Stand Attributes</li>
            )}
          </ul>
        </div> */
  
}

export default Delete;
