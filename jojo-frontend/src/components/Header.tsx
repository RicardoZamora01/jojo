import jojos from "../assets/wallpaper.jpeg";

const Header = () => {
  const handleClick = () => {
    console.log("click")
    const element = document.getElementById("all-stands");
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
      console.log(element)
    };
  };


  return (
    <div
      className="hero hero-h"
      style={{
        backgroundImage: `url(${jojos})`,
      }}
    >
      <div className="hero-overlay hero-h bg-opacity-60"></div>
      <div className="hero-content text-center text-indigo-50">
        <div className="max-w-md">
          <h1 className="mb-5 text-5xl font-bold">Discover, The World</h1>
          <p className="mb-5">
            Discover the captivating realm of JoJo's Bizarre Adventure. Meet its
            iconic characters, unravel the mysteries of their unique Stands, and
            explore the astonishing statistics and abilities.
          </p>
          <button className="btn btn-primary" onClick={handleClick}>Get Started</button>
        </div>
      </div>
    </div>
  );
};

export default Header;
