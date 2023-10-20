import jjbaLogo from "../assets/jjba_logo.png";
import "../styles/test.css";

const Navbar = () => {
  return (
    <div className="navbar bg-base-100 my-2">
      <button
        className="w-20 aspect-auto"
        onClick={() => {
          console.log("clicked");
        }}
      >
        <img src={jjbaLogo} alt="jojo logo"/>
      </button>
      
      <div className="flex-1">
        <label className="text-center font-bold px-6 text-xl">
          Jojo's Bizarre Adventure
        </label>
      </div>
      <div className="flex-none gap-2">
        <div className="form-control">
          <input
            type="text"
            placeholder="Search"
            className="input input-bordered w-24 md:w-auto mx-4"
          />
        </div>
      </div>
    </div>
  );
};

export default Navbar;
