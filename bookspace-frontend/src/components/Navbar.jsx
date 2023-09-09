import { useState } from 'react'

import { close, menu } from '../assets'
import { navLinks } from '../constants'

const Navbar = () => {
  const [active, setActive] = useState('Catalog')
  const [toggle, setToggle] = useState(false)

  return (
    <nav className="w-full flex py-6 justify-between items-centee navbar">
      <ul className="list-none sm:flex hidden justify-center items-center flex-1">
        {navLinks.map((nav, index) => (
          <li
            key={nav.id}
            className={`cursor-pointer text-[16px] ${
              active === nav.title ? 'text-cyan-400' : 'text-blue-800'
            } ${index === navLinks.length - 1 ? 'mr-0' : 'mr-10'}`}
            onClick={() => setActive(nav.title)}
          >
            <a href={`#${nav.id}`}>{nav.title}</a>
          </li>
        ))}
      </ul>

      <div className="text-blue-800">
        <a href="">Hello, sign in</a>
      </div>

      {/* Humbuger menu */}
      <div className="sm:hidden flex flex-1 justify-end items-center">
        <img
          src={toggle ? close : menu}
          alt="menu"
          className="w-[28px] h-[28px] object-contain"
          onClick={() => setToggle(!toggle)}
        />

        <div
          className={`${
            !toggle ? 'hidden' : 'flex'
          } p-6 bg-blue-800 absolute top-20 right-0 mx-4 my-2 min-w-[140px] rounded-xl flex-col`}
        >
          {navLinks.map((nav, index) => (
            <li
              key={nav.id}
              className={`cursor-pointer text-[16px] ${
                active === nav.title ? 'text-cyan-200' : 'text-white'
              } ${index === navLinks.length - 1 ? 'mb-0' : 'mb-4'}`}
              onClick={() => setActive(nav.title)}
            >
              <a href={nav.id}>{nav.title}</a>
            </li>
          ))}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
