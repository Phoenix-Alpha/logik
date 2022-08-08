import { SiteFooter, SiteHeader } from '@components'
import { Layout } from 'antd'
import { FC, ReactNode } from 'react'
import styled from 'styled-components'

const StyledSiteLayout = styled(Layout)`
  height: 100vh;
`
export interface ISiteLayoutProps {
  children?: ReactNode
}

export const SiteLayout: FC<ISiteLayoutProps> = ({ children }: ISiteLayoutProps) => {
  return (
    <StyledSiteLayout>
      <SiteHeader />
      <Layout.Content>{children}</Layout.Content>
      <SiteFooter />
    </StyledSiteLayout>
  )
}


SiteLayout.displayName = 'SiteLayout'

export default SiteLayout
