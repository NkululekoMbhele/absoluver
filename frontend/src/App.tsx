import React, {useState, useEffect} from 'react';

function App() {
  const [solution, setSolution] = useState({})
  const [error, setError] = useState()
  const [errorMessage, setErrorMessage] = useState("Please enter a valid equation!")
  const [equation, setEquation] = useState("")
  const validation = (equation: string) => {
    let status = true
    for (let i = 0; i < equation.length; i++) {
      if ((equation.indexOf("=") === equation.length - 1 ) || (equation.indexOf("=") === 0 )) {
        status = false
      }
      if (equation.indexOf("=") === 0 ) {
        status = false
      }
      console.log(equation[i]);
    }
    return status
  }
  const handleSubmit = async (e: React.ChangeEvent<any>) => {
    if (!validation(equation)) {
      console.log("Validated False")
      return
    }
    // e.preventDefault();
    console.log("Pressed")
    const requestOptions = {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch(`http://localhost:5000/?equation=${equation}`, requestOptions)
    const data = await response.json()
    console.log(data)
    setEquation("")
    }  
  const solutions = ["Add 2 to both sides", "Simplify", "Divide both sides by same factor 7", " Simplify", "Solution"]
  return (
    <div className="w-screen py-8 bg-gradient-to-t from-blue-300 via-green-200 to-yellow-300">
        <div className="container flex flex-col items-center w-full">
          <div className="grid w-full header place-items-center">
            <img src="https://firebasestorage.googleapis.com/v0/b/nkululekodotio-2b22e.appspot.com/o/absoluver%2Flogo.svg?alt=media&token=bce21cd0-c32a-4a7c-b5f6-5ab68c3080b2" alt="logo" />
            <h1 className="pt-4 text-4xl font-bold text-blue-600">ABSOLUVER</h1>
            <p className="pt-1 text-sm font-light tracking-wider text-blue-600">ABSOLUTE EQUATION SOLVER</p>
          </div>
          <div className="form">
            <form action="" className="flex flex-col items-center justify-center w-full py-4" onSubmit={handleSubmit}>
                <div className="flex border">
                      <input onChange={(e) => setEquation(e.target.value)} value={equation} type="text" className="px-4 py-2 border-none rounded-l w-72 focus:outline-none" placeholder="Equation" />
                      <button type="submit" className="flex items-center justify-center px-6 ml-auto font-bold text-white bg-blue-400 border-l rounded-r">
                          Solve
                      </button>
                </div>
                <h1 className="pt-2 text-red-400">{errorMessage}</h1>
              </form>
          </div>
          <section className="grid w-full py-4 solution place-items-center">
            <div className="flex flex-col items-center px-4 py-4 my-2 bg-white rounded-md shadow-md problem w-72">
                <h5 className="text-xl">Solve for x</h5>
                <h6 className="text-sm">7x - 2 = 21</h6>
            </div>
            {
            solutions.map(( value, key) => {
              return <div key={key} className="flex items-center w-11/12 px-4 py-4 my-2 bg-white rounded-md shadow-md problem md:w-1/2 sm:w-8/12">
                        <div className="grid w-8 h-8 text-sm text-center text-blue-500 border border-blue-500 rounded-full steps place-items-center">{key}</div>
                        <div className="flex flex-col pl-4 step">
                            <h5 className="text-md ">{value}</h5>
                            <h6 className="pt-2 text-sm">7x - 2 = 21</h6>
                        </div>
                      </div>
              })
            }
          </section>
        </div>
    </div>
  );
}
export default App;
