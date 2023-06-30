import { useEffect, useState, Fragment } from 'react'
import { Host, NetInterface, api } from './api'
import { Listbox, Transition } from '@headlessui/react'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid'

function App() {


  const [interfaces, setInterfaces] = useState<NetInterface[]>([])
  const [warning, setWarning] = useState('')
  const [selectedInterface, setSelectedInterface] = useState<NetInterface>()
  const [hosts, setHosts] = useState<Host[]>([])
  const [loading, setLoading] = useState(false)


  useEffect(() => {
    async function loadInterfaces() {
      const res = await api.get('/interfaces')
      setInterfaces(res.data.interfaces)
      setSelectedInterface(res.data.default ?? null)
    }
    loadInterfaces()
  }, [])

  useEffect(() => {
    if (String(selectedInterface?.prefix_length) !== '24') {
      setWarning('Warning! selected network is very large, consider choosing other.')
    } else {
      setWarning('')
    }
  }, [selectedInterface])

  async function scan() {
    setLoading(true)
    const res = await api.post('/scan', selectedInterface)
    const hosts = res.data as Host[]
    setHosts(hosts)
    setLoading(false)
  }

  return (
    <div className='m-auto w-[90%] lg:w-[800px] pt-8 flex flex-col align-center'>
      <span className='text-center m-auto text-2xl font-bold'>Mscan</span>
      <div className="">
        <Listbox value={selectedInterface} onChange={setSelectedInterface}>
          <div className="relative mt-1">
            <Listbox.Button className="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm">
              <span className="block truncate">{selectedInterface?.name}</span>
              <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                <ChevronUpDownIcon
                  className="h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
              </span>
            </Listbox.Button>
            <Transition
              as={Fragment}
              leave="transition ease-in duration-100"
              leaveFrom="opacity-100"
              leaveTo="opacity-0"
            >
              <Listbox.Options className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                {interfaces.map((iface, ifaceIdx) => (
                  <Listbox.Option
                    key={ifaceIdx}
                    className={({ active }) =>
                      `relative cursor-default select-none py-2 pl-10 pr-4 ${active ? 'bg-amber-100 text-amber-900' : 'text-gray-900'
                      }`
                    }
                    value={iface}
                  >
                    {({ selected }) => (
                      <>
                        <span
                          className={`block truncate ${selected ? 'font-medium' : 'font-normal'
                            }`}
                        >
                          {iface.name}
                        </span>
                        {selected ? (
                          <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-600">
                            <CheckIcon className="h-5 w-5" aria-hidden="true" />
                          </span>
                        ) : null}
                      </>
                    )}
                  </Listbox.Option>
                ))}
              </Listbox.Options>
            </Transition>
          </div>
        </Listbox>
      </div>
      {warning && (
        <span className='text-center mt-2 text-red-400'>
          {warning}
          </span>
      )}
      <button onClick={scan} type="button" className="my-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
        {loading ? (
          <svg aria-hidden="true" role="status" className="inline w-4 h-4 mr-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB" />
            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor" />
          </svg>
        ) : 'Scan'}

      </button>

      <ul role="list" className="divide-y divide-gray-100">
        {hosts.map(host => (
          <li key={host.ip} className="flex justify-between gap-x-6 py-5 flex-col text-center lg:flex-row items-center">
           <svg xmlns="http://www.w3.org/2000/svg" className='h-8 w-8' viewBox="0 0 640 512"><path d="M384 96V320H64L64 96H384zM64 32C28.7 32 0 60.7 0 96V320c0 35.3 28.7 64 64 64H181.3l-10.7 32H96c-17.7 0-32 14.3-32 32s14.3 32 32 32H352c17.7 0 32-14.3 32-32s-14.3-32-32-32H277.3l-10.7-32H384c35.3 0 64-28.7 64-64V96c0-35.3-28.7-64-64-64H64zm464 0c-26.5 0-48 21.5-48 48V432c0 26.5 21.5 48 48 48h64c26.5 0 48-21.5 48-48V80c0-26.5-21.5-48-48-48H528zm16 64h32c8.8 0 16 7.2 16 16s-7.2 16-16 16H544c-8.8 0-16-7.2-16-16s7.2-16 16-16zm-16 80c0-8.8 7.2-16 16-16h32c8.8 0 16 7.2 16 16s-7.2 16-16 16H544c-8.8 0-16-7.2-16-16zm32 160a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg>
            <div className="min-w-0 flex-auto w-[100px] overflow-auto">
              <p className="text-sm font-semibold leading-6 text-gray-900">IP</p>
              <p className="mt-1 truncate text-xs leading-5 text-gray-500">{host.ip}</p>
            </div>
            <div className="min-w-0 flex-auto w-[100px] overflow-auto">
              <p className="text-sm font-semibold leading-6 text-gray-900">HOSTNAME</p>
              <p className="mt-1 truncate text-xs leading-5 text-gray-500">{host.hostname}</p>
            </div>
            <div className="min-w-0 flex-auto w-[100px] overflow-auto">
              <p className="text-sm font-semibold leading-6 text-gray-900">MAC</p>
              <p className="mt-1 truncate text-xs leading-5 text-gray-500">{host.mac}</p>
            </div>
            <div className="min-w-0 flex-auto text-center w-[100px] overflow-auto">
              <p className="text-sm font-semibold leading-6 text-gray-900">Vendor</p>
              <p className="mt-1 truncate text-xs leading-5 text-gray-500">{host.vendor}</p>
            </div>
          </li>
        ))}

      </ul>
    </div>
  )
}

export default App
