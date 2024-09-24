/* eslint-disable react/no-is-mounted */

const htmlContainer = '.order-form'
const htmlOrderSummary = `${htmlContainer} .order-form__totals`
const htmlInputLines = `${htmlContainer} input[type="hidden"][name^="lines"]`
const htmlOptionsCertificates = `${htmlContainer} input[type="checkbox"][id^="certificate"]`
const htmlOptionsFees = `${htmlContainer} input[type="checkbox"][id^="fee"]`
const htmlInputPropertyId = `${htmlContainer} input[name="property_id"]`

const htmlSectionCertificates = `${htmlContainer} .order-form__section-certificates`
const htmlSectionCustomer = `${htmlContainer} .order-form__section-customer`
const htmlSectionFinal = `${htmlContainer} .order-form__section-finalise`
const htmlButtonNext = '.button-next'

const classHidden = 'is-hidden'

// Update totals with selected options.
function updateTotals () {
  let subtotal = 0
  let taxTotal = 0

  const selectedCertificates = document.querySelectorAll(
    `${htmlOptionsCertificates}:checked`
  )

  const selectedFees = document.querySelectorAll(
    `${htmlOptionsFees}:checked`
  )

  selectedCertificates.forEach((item) => {
    const price = parseFloat(item.dataset.price)
    const taxRate = parseFloat(item.dataset.taxRate) / 100
    const itemTax = price * taxRate
    console.debug(`Selected certificate: ${item.value}, Price: ${price}, Tax Rate: ${taxRate}, Tax: ${itemTax}`)
    subtotal += price
    taxTotal += itemTax
  })

  selectedFees.forEach((item) => {
    const price = parseFloat(item.dataset.price)
    const taxRate = parseFloat(item.dataset.taxRate) / 100
    const itemTax = price * taxRate
    console.debug(`Selected fee: ${item.name}, Price: ${price}, Tax Rate: ${taxRate}, Tax: ${itemTax}`)
    subtotal += price
    taxTotal += itemTax
  })

  const total = subtotal + taxTotal
  console.debug(`Subtotal: ${subtotal}, Tax: ${taxTotal}, Total: ${total}`)

  updateSummary(subtotal, taxTotal, total)
}

function updateSummary (subtotal, taxTotal, total) {
  const summaryElement = document.querySelector(htmlOrderSummary)
  if (summaryElement) {
    // Clear existing content
    summaryElement.textContent = ''

    // Create and append subtotal
    const subtotalElement = document.createElement('p')
    subtotalElement.textContent = `Subtotal: $${subtotal.toFixed(2)}`
    summaryElement.appendChild(subtotalElement)

    // Create and append tax
    const taxElement = document.createElement('p')
    taxElement.textContent = `Tax: $${taxTotal.toFixed(2)}`
    summaryElement.appendChild(taxElement)

    // Create and append total
    const totalElement = document.createElement('p')
    totalElement.textContent = `Total: $${total.toFixed(2)}`
    summaryElement.appendChild(totalElement)
  }
}

// Update order lines with selected options.
function updateLines () {
  const order = {}

  const selectedCertificates = Array.from(
    document.querySelectorAll(
      `${htmlOptionsCertificates}:checked`
    )
  )

  const selectedFees = Array.from(
    document.querySelectorAll(`${htmlOptionsFees}:checked`)
  )

  selectedCertificates.forEach(selectedCertificate => {
    const certId = parseInt(selectedCertificate.value)
    order[certId] = { certificate_id: certId, fee_id: undefined }
  })

  selectedFees.forEach(selectedFee => {
    const certId = selectedFee.dataset.certificate
    const feeId = parseInt(selectedFee.value)
    if (certId && order[certId]) order[certId].fee_id = feeId
  })

  const data = Object.values(order)
  const linesJson = document.querySelector(htmlInputLines)
  linesJson.value = JSON.stringify(data)
}

export class OrderForm {
  inputPropertyId = null
  elemSectionCertificates = null
  elemSectionCustomer = null
  elemSectionFinal = null

  activate () {
    this.elemSectionCertificates.classList.remove(classHidden)
  }

  deactivate () {
    this.elemSectionCertificates.classList.add(classHidden)
    this.elemSectionCustomer.classList.add(classHidden)
    this.elemSectionFinal.classList.add(classHidden)
  }

  bindSteps () {
    const steps = [
      this.elemSectionCertificates,
      this.elemSectionCustomer,
      this.elemSectionFinal
    ]

    steps.forEach((section, index) => {
      const submit = section.querySelector(htmlButtonNext)
      const next = steps[index + 1]
      if (submit && next) {
        submit.addEventListener('click', (event) => {
          event.preventDefault()
          next.classList.remove(classHidden)
        })
      }
    })
  }

  constructor () {
    this.inputPropertyId = document.querySelector(htmlInputPropertyId)

    this.elemSectionCertificates = document.querySelector(htmlSectionCertificates)
    this.elemSectionCustomer = document.querySelector(htmlSectionCustomer)
    this.elemSectionFinal = document.querySelector(htmlSectionFinal)

    this.deactivate()
    this.bindSteps()

    const optionsAll = document.querySelectorAll(
      `${htmlOptionsCertificates}, ${htmlOptionsFees}`
    )

    optionsAll.forEach((checkbox) => {
      checkbox.addEventListener('change', updateTotals)
      checkbox.addEventListener('change', updateLines)
    })

    updateTotals()
    updateLines()

    const form = document.querySelector(htmlContainer)
    console.log('Form found:', form)
    if (form) {
      form.addEventListener('submit', this.handleSubmit.bind(this))
      console.log('Submit event listener added')
    } else {
      console.error('Form not found')
    }
  }

  handleSubmit (event) {
    console.log('Form submission started')
    event.preventDefault()
    const formData = new FormData(event.target)
    const propertyId = this.inputPropertyId.value
    console.log('Property ID:', propertyId)

    fetch(event.target.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
      }
    })
      .then(response => {
        console.log('Response received:', response)
        if (response.headers.get('Content-Type').includes('application/json')) {
          return response.json()
        } else {
          return response.text().then(text => {
            console.log('Received HTML:', text)
            throw new Error('Received HTML instead of JSON')
          })
        }
      })
      .then(data => {
        console.log('Parsed data:', data)
        if (data.errors) {
          this.displayErrors(data.errors)
          this.inputPropertyId.value = propertyId
          this.activate()
        } else if (data.redirect_url) {
          window.location.href = data.redirect_url
        } else {
          console.error('Unexpected response format:', data)
        }
      })
      .catch(error => {
        console.error('Fetch error:', error)
        this.displayErrors({ __all__: ['An unexpected error occurred. Please try again.'] })
        this.inputPropertyId.value = propertyId
        this.activate()
      })
  }

  displayErrors (errors) {
    console.error('Form submission errors:', errors)

    let errorContainer = document.querySelector('.order-form__error')
    if (!errorContainer) {
      const form = document.querySelector('.order-form')
      errorContainer = document.createElement('div')
      errorContainer.className = 'order-form__error error'
      form.insertBefore(errorContainer, form.firstChild)
    }

    errorContainer.innerHTML = ''

    if (errors.__all__) {
      errors.__all__.forEach(error => {
        const errorElement = document.createElement('div')
        errorElement.textContent = error
        errorContainer.appendChild(errorElement)
      })
    }

    errorContainer.style.display = 'block'
  }
}
