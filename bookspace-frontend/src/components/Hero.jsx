import { logo } from '../assets'
import readImage from '../assets/read.png'
import catalogImage from '../assets/catalog.png'
import listenImage from '../assets/listen.png'

const Hero = () => {
  return (
    <div className="mt-[70px] w-full">
      <h1 className="text-3xl text-center text-blue-800 mb-8">
        We have the exact book you're looking for
      </h1>

      <div className="flex flex-col sm:flex-row justify-center items-center gap-8">
        {/* Card 1 */}
        <div className="bg-white shadow-xl rounded-lg p-6 text-center w-64">
          <img
            src={readImage}
            alt="read"
            className="h-48 w-full rounded-lg mb-4"
          />
          <button className="bg-cyan-300 text-blue-800 px-4 py-2 rounded hover:text-zinc-900 transition">
            Read
          </button>
        </div>

        {/* Card 2 */}
        <div className="bg-white shadow-xl rounded-lg p-6 text-center w-64">
          <img
            src={catalogImage}
            alt="Catalog"
            className="h-48 w-full mx-auto mb-4"
          />
          <button className="bg-cyan-300 text-blue-800 px-4 py-2 rounded hover:text-zinc-900 transition">
            Catalog
          </button>
        </div>

        {/* Card 3 */}
        <div className="bg-white shadow-xl rounded-lg p-6 text-center w-64">
          <img
            src={listenImage}
            alt="listen"
            className="h-48 w-full mx-auto mb-4"
          />
          <button className="bg-cyan-300 text-blue-800 px-4 py-2 rounded hover:text-zinc-900 transition">
            Listen
          </button>
        </div>
      </div>
    </div>
  )
}

export default Hero
