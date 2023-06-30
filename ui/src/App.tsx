import { useEffect, useState, Fragment } from 'react'
import { Host, NetInterface, api } from './api'
import { Listbox, Transition } from '@headlessui/react'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid'
import { Dialog } from '@headlessui/react'

function App() {


  const [interfaces, setInterfaces] = useState<NetInterface[]>([])
  const [selectedInterface, setSelectedInterface] = useState<NetInterface>()
  const [hosts, setHosts] = useState<Host[]>([])
  const [isOpen, setIsOpen] = useState(true)


  useEffect(() => {
    async function loadInterfaces() {
      const res = await api.get('/interfaces')
      setInterfaces(res.data.interfaces)
      setSelectedInterface(res.data.default ?? null)
    }
    loadInterfaces()
  }, [])

  async function scan() {
    const res = await api.post('/scan', selectedInterface)
    const hosts = res.data as Host[]
    setHosts(hosts)
  }

  return (
    <>
      <Dialog open={isOpen} onClose={() => setIsOpen(false)} className="relative z-50">
        {/* The backdrop, rendered as a fixed sibling to the panel container */}
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />

        <div className="fixed inset-0 flex items-center justify-center p-4">

          <Dialog.Panel className="w-full max-w-sm rounded bg-white">
            <Dialog.Title>Deactivate account</Dialog.Title>
            <Dialog.Description>
              This will permanently deactivate your account
            </Dialog.Description>

            <p>
              Are you sure you want to deactivate your account? All of your data
              will be permanently removed. This action cannot be undone.
            </p>

            <button onClick={() => setIsOpen(false)}>Deactivate</button>
            <button onClick={() => setIsOpen(false)}>Cancel</button>
          </Dialog.Panel>
        </div>
      </Dialog>
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
      <button onClick={scan} type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Scan</button>
      <table>
        <thead>
          <tr>
            <th>ip</th>
            <th>hostname</th>
            <th>mac</th>
            <th>vendor</th>
          </tr>
        </thead>
        <tbody>
          {hosts.map(host => (
            <tr key={host.ip}>
              <td>{host.ip}</td>
              <td>{host.hostname}</td>
              <td>{host.mac}</td>
              <td>{host.vendor}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export default App
