import { MenuOutlined } from '@ant-design/icons'
import { SiteDrawer } from '@components'
import { META_DEFAULTS } from '@configs/misc'
import { Button, Layout, Row } from 'antd'
import { FC, useState } from 'react'
import styled from 'styled-components'


const StyledSiteHeader = styled(Layout.Header)`
  background-color: white;
  border: 1px solid rgb(139 139 139);
  padding: 0 20px;
`

export interface ISiteHeaderProps {}

export const SiteHeader: FC<ISiteHeaderProps> = ({}: ISiteHeaderProps) => {
  const [drawerVisible, setDrawerVisible] = useState(false)

  const toggleDrawer = () => {
    setDrawerVisible(!drawerVisible)
  }

  const closeDrawer = () => {
    setDrawerVisible(false)
  }

  return (
    <StyledSiteHeader>
      <Row align="middle">
        <Button type="text" icon={<MenuOutlined />} onClick={toggleDrawer} />
        {META_DEFAULTS.title}
      </Row>
      <SiteDrawer visible={drawerVisible} closeDrawer={closeDrawer} />
    </StyledSiteHeader>
  )
}

SiteHeader.displayName = 'SiteHeader'

export default SiteHeader
