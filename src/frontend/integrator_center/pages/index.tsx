import { SiteHead, SiteLayout, Welcome } from '@components'
import { NextPage } from 'next'

export interface IHomePageProps {}

export const HomePage: NextPage<IHomePageProps> = () => {
  return (
    <>
      <SiteHead title="Integrator Center" />
      <SiteLayout>
        <Welcome />
      </SiteLayout>
    </>
  )
}

HomePage.displayName = 'HomePage'

export default HomePage
