import React, {useState, useEffect} from 'react';

function App() {
  const [data, setData] = useState({})
  const [solution, setSolution] = useState({})
  const [steps, setSteps] = useState([])
  const [variable, setVariable] = useState("")
  const [equat, setEquat] = useState("")
  const [errorMessage, setErrorMessage] = useState("")
  const [equation, setEquation] = useState("")

  // Handle Form Submission
  const handleSubmit = async (e: React.ChangeEvent<any>) => {
    e.preventDefault()
    console.log(equation)
    let decodedEquation = equation.replace("+", "%2B")
    decodedEquation = decodedEquation.replace("-", "%2D")
    decodedEquation = decodedEquation.replace("=", "%3D")
    decodedEquation = decodedEquation.replace("*", "%2A")
    decodedEquation = decodedEquation.replace("+", "%2B")
    decodedEquation = decodedEquation.replace("(", "%28")
    decodedEquation = decodedEquation.replace(")", "%29")
    console.log(decodedEquation)
    const response = await fetch(`http://127.0.0.1:8080/?equation=${decodedEquation}`)
    const data = await response.json()
    console.log(data)
    setData(data)
    setSteps(data.steps)
    setVariable(data.variable)
    setEquat(data.equation)
    console.log(data.steps[0].step)
    setEquation("")
  }
  return (
    <div className="w-screen min-h-screen py-8 bg-gradient-to-t from-blue-300 via-green-200 to-yellow-300">
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
                {/* <ChangeColor /> */}
              </form>

          </div>
          <section className="grid w-full py-4 solution place-items-center">
            {
              (steps.length !== 0) && (
              <div className="flex flex-col items-center px-4 py-4 my-2 bg-white rounded-md shadow-md problem w-72">
                  <h5 className="text-xl">Solve for {variable}</h5>
                  <h6 className="text-sm">{equat}</h6>
              </div>)
            }
            {
            (steps) && 
            steps.map((value: any, key) => {
              return <div key={key} className="flex items-center w-11/12 px-4 py-4 my-2 bg-white rounded-md shadow-md problem md:w-1/2 sm:w-8/12">
                        <div className="grid w-8 h-8 text-sm text-center text-blue-500 border border-blue-500 rounded-full steps place-items-center">{value.step_count}</div>
                          <div className="flex flex-col pl-4 step">
                              <h5 className="text-md ">{value.step}</h5>
                              <h6 className="pt-2 text-sm">{document.createElement('div').innerHTML = value.step_equation}</h6>
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


const ChangeColor = (props: any) => {
  let equation = "2x - 5 = 5"
  equation.replace("- 5", "- 6")
  let text = <h1>{`${equation}`}</h1>
  return (
  <>
    {text}
  </>
  )
} 