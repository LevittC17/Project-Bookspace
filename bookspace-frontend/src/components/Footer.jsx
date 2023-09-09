import styles from '../style'
/* import { logo } from '../assets' */
import logoiconImage from '../assets/logoicon.png'
import { footerLinks, socialMedia } from '../constants'

const Footer = () => (
  <section
    className={`bg-cyan-200 ${styles.flexCenter} ${styles.paddingY} flex-col`}
  >
    <div className={`${styles.flexStart} md:flex-row flex-col mb-8 w-full`}>
      <div className="flex-[1] flex flex-col justify-start mr-10">
        <div className="flex flex-wrap text-blue-800 w-full sm:w-4/5">
          <img src={logoiconImage} alt="Bookspace Logo" className="logo" />
          <h1 className="text-2xl sm:text-4xl">BOOKSPACE</h1>
        </div>

        <p className={`${styles.paragraph} text-black pl-8 mt-4 max-w-[312px]`}>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Nihil
          suscipit
        </p>
      </div>

      <div className="text-zinc-900 flex-[1.5] w-full flex flex-row justify-between flex-wrap md:mt-0 mt-10 ml-2">
        {footerLinks.map((footerlink) => (
          <div
            key={footerlink.title}
            className={`flex flex-col ss:my-0 my-4 min-w-[150px]`}
          >
            <h4 className="font-bold text-[18px] leading-[27px] text-blue-800 ">
              {footerlink.title}
            </h4>
            <ul className="list-none mt-4">
              {footerlink.links.map((link, index) => (
                <li
                  key={link.name}
                  className={`font-poppins font-normal text-[16px] leading-[24px] text-dimWhite hover:text-secondary cursor-pointer ${
                    index !== footerlink.links.length - 1 ? 'mb-4' : 'mb-0'
                  }`}
                >
                  {link.name}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>

    <div className="w-full flex justify-between items-center md:flex-row flex-col pt-6 border-t-[1px] border-t-[#3F3E45]">
      <p className="font-poppins font-normal text-center text-[18px] leading-[27px] text-zinc-900 pl-8">
        Copyright Ⓒ 2023 BookSpace. All Rights Reserved.
      </p>

      <div className="flex flex-row md:mt-0 mt-6 mr-2">
        {socialMedia.map((social, index) => (
          <img
            key={social.id}
            src={social.icon}
            alt={social.id}
            className={`w-[21px] h-[21px] object-contain cursor-pointer bg-black ${
              index !== socialMedia.length - 1 ? 'mr-6' : 'mr-0'
            }`}
            onClick={() => window.open(social.link)}
          />
        ))}
      </div>
    </div>
  </section>
)

export default Footer
