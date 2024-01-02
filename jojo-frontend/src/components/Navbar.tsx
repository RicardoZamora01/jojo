import { ChangeEvent, useState } from "react";
import jjbaLogo from "../assets/jjba_logo.png";
import "../styles/test.css";

interface SearchResult {
  id: number;
  character_name: string;
}

const Navbar = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  const handleSearch = async (query: string) => {
    try {
      const response = await fetch(`/characters?search=${query}`);
      const data = await response.json();
      // setSearchResults(data); // Update state with search results
      if (Array.isArray(data) && data.length > 0 && query.length > 0) {
        const results: SearchResult[] = data.map((result: any) => ({
          id: data.indexOf(result),
          character_name: result[0],
        }));
        setSearchResults(results);
      } else {
        setSearchResults([]);
      }
      console.log(searchResults);

      // searchResults.map((result) => (
      //   console.log(result.character_name)
      // ))
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchTerm(query); // Update search term in state
    handleSearch(query); // Perform search on each input change
  };

  return (
    <div className="navbar bg-base-100 my-2">
      <button
        className="w-20 aspect-auto"
        onClick={() => {
          console.log("clicked");
        }}
      >
        <img src={jjbaLogo} alt="jojo logo" />
      </button>

      <div className="flex-1">
        <label className="text-center font-bold px-6 text-xl">
          Jojo's Bizarre Adventure
        </label>
      </div>
      <div className="flex-none gap-2">
        <div className="form-control relative">
          <input
            type="text"
            placeholder="Search"
            className="input input-bordered w-24 md:w-auto mx-4 "
            value={searchTerm}
            onChange={handleChange}
          />
          <ul
            className="absolute top-10 right-4 py-2 z-10 overflow-y-auto max-h-72"
            style={{ width: document.querySelector(".input")?.clientWidth }}
          >
            {searchResults.map((result) => (
              <li
                className="border-solid border-slate-500 border-[1px] rounded-md bg-neutral bg-opacity-90 hover:bg-opacity-100 hover:text-white hover:bg-primary-focus hover:cursor-pointer py-2 px-1 "
                key={result.id}
              >
                {result.character_name}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
